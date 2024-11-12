package ar.edu.utn.frc.backend.services;

import ar.edu.utn.frc.backend.distancias.*;
import ar.edu.utn.frc.backend.dto.DTOActualizarPosicion;
import ar.edu.utn.frc.backend.dto.DTOReporteIncidente;
import ar.edu.utn.frc.backend.dto.DTONotificacion;
import ar.edu.utn.frc.backend.dtosApiExterna.DTOCoordenada;
import ar.edu.utn.frc.backend.dtosApiExterna.DTOPosicionAPI;
import ar.edu.utn.frc.backend.entities.Posicion;
import ar.edu.utn.frc.backend.entities.Vehiculo;
import ar.edu.utn.frc.backend.repositorios.EmpleadoRepositorio;
import ar.edu.utn.frc.backend.repositorios.PosicionRepositorio;
import ar.edu.utn.frc.backend.repositorios.PruebaRepositorio;
import ar.edu.utn.frc.backend.repositorios.VehiculoRepositorio;
import lombok.extern.slf4j.Slf4j;
import org.hibernate.service.spi.ServiceException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Slf4j
@Service
public class PosicionService {

    private final Zona zonaGeografica;
    private final APIExternaService apiExternaService;
    private final RestTemplate restTemplate;
    private final DTOPosicionAPI dtoPosicionAPI;
    private final PruebaService pruebaService;
    private final PruebaRepositorio pruebaRepositorio;
    private final PosicionRepositorio posicionRepositorio;
    private final EmpleadoRepositorio empleadoRepositorio;
    private final VehiculoRepositorio vehiculoRepositorio;
    private final ReporteService reporteService;
    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    // URL del microservicio de notificaciones
    private final String notificacionUrl = "http://localhost:8083/api/notificaciones";

    @Autowired
    public PosicionService(APIExternaService apiExternaService,
                           RestTemplate restTemplate,
                           PruebaService pruebaService,
                           ReporteService reporteService,
                           PosicionRepositorio posicionRepositorio,
                           PruebaRepositorio pruebaRepositorio,
                           EmpleadoRepositorio empleadoRepositorio, VehiculoRepositorio vehiculoRepositorio) {
        this.empleadoRepositorio = empleadoRepositorio;
        this.vehiculoRepositorio = vehiculoRepositorio;
        this.zonaGeografica = new Zona();
        this.apiExternaService = apiExternaService;
        this.restTemplate = restTemplate;
        this.dtoPosicionAPI = new DTOPosicionAPI();
        this.pruebaService = pruebaService;
        this.reporteService = reporteService;
        this.posicionRepositorio = posicionRepositorio;
        this.pruebaRepositorio = pruebaRepositorio;
    }

    // Servicio para cargar todas las zonas restringidas de la api
    public DTOPosicionAPI cargarZonasDesdeAPI() throws ServiceException {
        DTOPosicionAPI configuracion = apiExternaService.getConfiguracionAPI();

        if (configuracion == null || configuracion.getZonasRestringidas() == null) {
            throw new RuntimeException("La configuración de la API externa es nula o inválida.");
        }

        for (var zona : configuracion.getZonasRestringidas()) {
            if (zona.getNoroeste() == null || zona.getSureste() == null) {
                throw new RuntimeException("Zona restringida con coordenadas nulas.");
            }

            Coordenada noroeste = new Coordenada(zona.getNoroeste().getLatitud(), zona.getNoroeste().getLongitud());
            Coordenada sureste = new Coordenada(zona.getSureste().getLatitud(), zona.getSureste().getLongitud());
            zonaGeografica.agregarZona(new Area(noroeste, sureste));
        }
        return configuracion;
    }

    public void enviarNotificacion(String mensaje, Long legajo) {
        try {
            String url = notificacionUrl + "/crear";

            // Crear el objeto NotificacionDTO
            DTONotificacion DTONotificacion = new DTONotificacion();
            DTONotificacion.setMensaje(mensaje);
            DTONotificacion.setLegajo(legajo);

            // Crear los encabezados para la solicitud JSON
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            // Crear la entidad con el cuerpo JSON y los encabezados
            HttpEntity<DTONotificacion> entity = new HttpEntity<>(DTONotificacion, headers);

            // Enviar la solicitud POST al microservicio de notificación
            ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.POST, entity, String.class);

            if (response.getStatusCode() == HttpStatus.OK) {
                log.info("Notificación enviada con éxito!");
            } else {
                log.warn("Notificación no enviada, código de estado: {}", response.getStatusCode());
            }

        } catch (HttpClientErrorException e) {
            log.error("Error al enviar la notificación al microservicio: HTTP Status: {}, Response Body: {}",
                    e.getStatusCode(), e.getResponseBodyAsString(), e);
        } catch (Exception e) {
            log.error("Error inesperado al enviar la notificación: {}", e.getMessage(), e);
        }
    }

    public boolean verificarPunto(Posicion posicion, DTOPosicionAPI dtoPosicionAPI, Long vehiculoId) {
        Coordenada punto = new Coordenada(posicion.getLatitud(), posicion.getLongitud());
        Long legajo = pruebaRepositorio.findEmpleadoIdByVehiculoId(vehiculoId);

        // Instanciar la zona y cargar las zonas desde la API
        Zona zonaGeografica = new Zona();
        zonaGeografica.cargarZonasDesdeAPI(dtoPosicionAPI);

        // Verificar si el punto está dentro de alguna zona restringida
        boolean dentroDeZonaRestringida = zonaGeografica.verificarPunto(punto);
        boolean dentroDelRadio = false;

        // Obtenemos las coordenadas de la agencia y el radio admitido
        DTOCoordenada coordenadasAgenciaDto = dtoPosicionAPI.getCoordenadasAgencia();
        Double radioAdmitidoKm = dtoPosicionAPI.getRadioAdmitidoKm();

        if (coordenadasAgenciaDto != null) {
            Coordenada coordenadasAgencia1 = new Coordenada(coordenadasAgenciaDto.getLatitud(), coordenadasAgenciaDto.getLongitud());

            // Calculamos la distancia entre la agencia y el vehículo
            Double distancia = ObtenerDistancia.calcularDistancia(coordenadasAgencia1, punto);

            // Si la distancia es menor o igual al radio admitido, el vehículo está dentro del radio
            if (distancia <= radioAdmitidoKm) {
                dentroDelRadio = true;
            }
        } else {
            log.info("coordenadas nulas");
        }

        // Si está dentro de una zona restringida o fuera del radio admitido, se envía notificación y actualiza estado
        if (dentroDeZonaRestringida || !dentroDelRadio) {
            enviarNotificacion("¡Atención!, Regresar el vehículo de manera inmediata.", legajo);

            pruebaService.actualizarEstadoInteresadoPorId(vehiculoId);

            // añadirlo a la lista de incidentes
            DTOReporteIncidente incidente = reporteService.obtenerDatosParaReporteIncidente(vehiculoId);
            reporteService.agregarIncidente(incidente);
        }

        // Retorna true si el punto está dentro de una zona restringida o fuera del radio de la agencia
        return dentroDeZonaRestringida || !dentroDelRadio;
    }

    public void agregarNuevaPosicion(Vehiculo vehiculo, DTOActualizarPosicion dtoActualizarPosicion) {
        // Verificar si los valores de latitud, longitud y patente son nulos
        if (dtoActualizarPosicion.getLatitud() == null || dtoActualizarPosicion.getLongitud() == null ||
                dtoActualizarPosicion.getPatente() == null) {
            throw new IllegalArgumentException("Todos los campos son obligatorios.");
        }

        LocalDateTime fechaHora = LocalDateTime.now();
        String fechaHoraFormateada = fechaHora.format(formatter);

        // Obtener latitud y longitud del DTO
        Double latitud = dtoActualizarPosicion.getLatitud();
        Double longitud = dtoActualizarPosicion.getLongitud();

        // Crear una nueva posición
        Posicion nuevaPosicion = new Posicion();
        nuevaPosicion.setVehiculo(vehiculo);
        nuevaPosicion.setLatitud(latitud);
        nuevaPosicion.setLongitud(longitud);
        nuevaPosicion.setFechaHora(fechaHoraFormateada);

        // Guardar la nueva posición en la base de datos
        posicionRepositorio.save(nuevaPosicion);

        // Agregar la nueva posición a la lista de posiciones del vehículo
        vehiculo.getPosiciones().add(nuevaPosicion);

        // Imprimir logs con la nueva posición
        log.info("Nueva posición del vehículo (ID: " + vehiculo.getId() + "): Latitud = " + latitud + ", Longitud = " + longitud);
        log.info("Posición del vehículo actualizada.");
    }
}