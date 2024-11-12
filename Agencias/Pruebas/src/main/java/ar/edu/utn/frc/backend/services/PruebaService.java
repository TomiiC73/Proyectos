package ar.edu.utn.frc.backend.services;

import ar.edu.utn.frc.backend.dto.*;
import ar.edu.utn.frc.backend.entities.*;
import ar.edu.utn.frc.backend.repositorios.*;
import jakarta.persistence.EntityNotFoundException;
import lombok.extern.slf4j.Slf4j;
import org.hibernate.service.spi.ServiceException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataAccessException;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Slf4j
@Service
public class PruebaService {

    private final PruebaRepositorio pruebaRepositorio;
    private final InteresadoRepositorio interesadoRepositorio;
    private final VehiculoRepositorio vehiculoRepositorio;
    private final EmpleadoRepositorio empleadoRepositorio;
    private final PosicionRepositorio posicionRepositorio;
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    @Autowired
    public PruebaService(PruebaRepositorio pruebaRepositorio,
                         InteresadoRepositorio interesadoRepositorio,
                         VehiculoRepositorio vehiculoRepositorio,
                         EmpleadoRepositorio empleadoRepositorio, PosicionRepositorio posicionRepositorio) {

        this.pruebaRepositorio = pruebaRepositorio;
        this.interesadoRepositorio = interesadoRepositorio;
        this.vehiculoRepositorio = vehiculoRepositorio;
        this.empleadoRepositorio = empleadoRepositorio;
        this.posicionRepositorio = posicionRepositorio;
    }

    // Servicio para crear una prueba, validando que exista el interesado, empleado y vehiculo
    public Prueba create(DTOCrearPrueba pruebaDTO) throws ServiceException {
        validatePruebaDTO(pruebaDTO);

        LocalDateTime fechaHoraInicio = LocalDateTime.now();
        String fechaHoraInicioFormateada = fechaHoraInicio.format(formatter);

        Interesado interesado = interesadoRepositorio.findById(pruebaDTO.getInteresadoId())
                .orElseThrow(() -> {
                    return new EntityNotFoundException("No se encontró el interesado con id " + pruebaDTO.getInteresadoId());
                });

        Empleado empleado = empleadoRepositorio.findById(pruebaDTO.getEmpleadoId())
                .orElseThrow(() -> {
                    return new EntityNotFoundException("No se encontró el empleado con id " + pruebaDTO.getEmpleadoId());
                });

        Vehiculo vehiculo = vehiculoRepositorio.findById(pruebaDTO.getVehiculoId())
                .orElseThrow(() -> {
                    return new EntityNotFoundException("No se encontró el vehículo con id " + pruebaDTO.getVehiculoId());
                });

        Optional<Prueba> pruebas = pruebaRepositorio.findPruebaByVehiculoIdAndFechaHoraFinIsNull(vehiculo.getId());
        if (pruebas.isPresent()) {
            String errorMessage = "El vehículo con id " + vehiculo.getId() + " está actualmente en uso en otra prueba.";
            log.error(errorMessage);
            throw new IllegalArgumentException(errorMessage);
        }

        try {
            // Crear una nueva posición con coordenadas 0, 0 para el vehículo
            Posicion posicion = new Posicion();
            posicion.setVehiculo(vehiculo);
            posicion.setLatitud(42.50886738457441);
            posicion.setLongitud(1.5347139324337429);
            posicion.setFechaHora(LocalDateTime.now().format(formatter));

            // Agregar la nueva posición a la lista de posiciones del vehículo
            vehiculo.getPosiciones().add(posicion);

            // Guardar la nueva posición en la base de datos
            posicionRepositorio.save(posicion);

            Prueba prueba = new Prueba();
            prueba.setVehiculo(vehiculo);
            prueba.setInteresado(interesado);
            prueba.setEmpleado(empleado);
            prueba.setFechaHoraInicio(fechaHoraInicioFormateada);
            pruebaRepositorio.save(prueba);

            return prueba;

        } catch (DataAccessException e) {
            throw new RuntimeException("Error al crear la prueba en la base de datos", e);
        }
    }

    // Funcion para validar que los datos ingresados no sean nulos
    private void validatePruebaDTO(DTOCrearPrueba pruebaDTO) {
        if (pruebaDTO.getVehiculoId() == null ||
                pruebaDTO.getInteresadoId() == null ||
                pruebaDTO.getEmpleadoId() == null) {
            throw new IllegalArgumentException("Todos los campos son obligatorios.");
        }
    }

    // Servicio para gestionar las pruebas en curso
    public List<DTOPruebaEnCurso> obtenerPruebasEnCurso() throws ServiceException {
        List<Prueba> pruebas = pruebaRepositorio.findByFechaHoraFinIsNull();

        return pruebas.stream().map(prueba ->
                new DTOPruebaEnCurso(
                        prueba.getVehiculo().getPatente(),
                        prueba.getInteresado().getNombre(),
                        prueba.getInteresado().getApellido(),
                        prueba.getEmpleado().getNombre(),
                        prueba.getEmpleado().getApellido(),
                        prueba.getFechaHoraInicio()
                )
        ).collect(Collectors.toList());
    }

    // Servicio para finalizar una prueba
    public Optional<Prueba> finalizarPrueba(Long idPrueba, String comentarios) throws ServiceException {
        Optional<Prueba> pruebaOpt = pruebaRepositorio.findById(idPrueba);

        if (pruebaOpt.isPresent()) {
            LocalDateTime fechaHoraFin = LocalDateTime.now();
            String fechaHoraFinFormateada = fechaHoraFin.format(formatter);

            Prueba prueba = pruebaOpt.get();
            prueba.setComentarios(comentarios);
            prueba.setFechaHoraFin(fechaHoraFinFormateada);
            return Optional.of(pruebaRepositorio.save(prueba));
        }
        return Optional.empty(); // Retorna vacío si no se encontró la prueba
    }

    public void actualizarEstadoInteresadoPorId(Long idVehiculo) {
        // Buscar la prueba activa asociada al vehículo con el ID proporcionado
        Optional<Prueba> pruebaOpt = pruebaRepositorio.findPruebaByVehiculoIdAndFechaHoraFinIsNull(idVehiculo);

        // Si no se encuentran pruebas, lanzar una excepción
        Prueba prueba = pruebaOpt.orElseThrow(() -> new IllegalArgumentException("No se encontró prueba en curso para el vehículo con id: " + idVehiculo));

        // Obtener el interesado relacionado con la prueba activa
        Interesado interesado = prueba.getInteresado();

        // Actualizar el estado del interesado a "restringido"
        interesado.setRestringido("true");

        // Guardar el interesado actualizado
        interesadoRepositorio.save(interesado);
    }

    public List<String> obtenerNrosTelefono() {
        return empleadoRepositorio.findTelefonos();
    }

    public String obtenerNroTelefono(Long legajo) {
        return empleadoRepositorio.findTelefonoByLegajo(legajo);
    }
}
