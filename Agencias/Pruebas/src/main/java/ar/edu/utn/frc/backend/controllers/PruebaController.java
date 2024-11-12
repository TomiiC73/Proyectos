package ar.edu.utn.frc.backend.controllers;

import ar.edu.utn.frc.backend.dto.DTOCrearPrueba;
import ar.edu.utn.frc.backend.dto.DTOPruebaEnCurso;
import ar.edu.utn.frc.backend.entities.Prueba;
import ar.edu.utn.frc.backend.services.PruebaService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Collections;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/pruebas")

public class PruebaController {

    @Autowired
    private PruebaService pruebaService;
    private static final Logger log = LoggerFactory.getLogger(PruebaController.class);

    @GetMapping("/saludo")
    public ResponseEntity<String> test() {
        return ResponseEntity.ok("Hola!");
    }

    // Endpoint para crear una prueba
    @PostMapping("/crear-prueba")
    public ResponseEntity<Prueba> createPrueba(@RequestBody DTOCrearPrueba pruebaDTO) {

        // Verificamos si faltan campos
        if (pruebaDTO.getVehiculoId() == null || pruebaDTO.getInteresadoId() == null || pruebaDTO.getEmpleadoId() == null) {
            log.error("Solicitud incompleta: falta un campo obligatorio. VehiculoId: {}, InteresadoId: {}, EmpleadoId: {}",
                    pruebaDTO.getVehiculoId(), pruebaDTO.getInteresadoId(), pruebaDTO.getEmpleadoId());

            return ResponseEntity.badRequest().build(); // Devuelve un 400 Bad Request si falta algún campo
        }

        try {
            // Llamada al servicio para crear la prueba
            Prueba pruebaCreada = pruebaService.create(pruebaDTO);

            return ResponseEntity.status(HttpStatus.CREATED).body(pruebaCreada); // Devuelve 201 Created

        } catch (Exception e) {
            // Log de error
            log.error("Error al crear la prueba: ", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null); // Devuelve 500 Internal Server Error
        }
    }

    // Endpoint para consultar pruebas en curso
    @GetMapping("/en-curso")
    public ResponseEntity<List<DTOPruebaEnCurso>> obtenerPruebasEnCurso() {
        try {
            List<DTOPruebaEnCurso> pruebas = pruebaService.obtenerPruebasEnCurso();
            if (pruebas.isEmpty()) {
                return ResponseEntity.status(HttpStatus.NO_CONTENT).build(); // 204 No Content si no hay pruebas
            }
            return ResponseEntity.ok(pruebas); // 200 OK si hay pruebas

        } catch (Exception e) {
            log.error("Error al obtener las pruebas: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build(); // 500 Internal Server Error
        }
    }

    // Endpoint para finalizar una prueba
    @PutMapping("/finalizar")
    public ResponseEntity<Prueba> finalizarPrueba(@RequestParam Long idPrueba,
                                                  @RequestParam String comentarios) {

        if (idPrueba == null || comentarios == null || comentarios.isEmpty()) {
            return ResponseEntity.badRequest().body(null);
        }

        try {
            Optional<Prueba> pruebaFinalizadaOpt = pruebaService.finalizarPrueba(idPrueba, comentarios);

            return pruebaFinalizadaOpt.map(ResponseEntity::ok)
                    .orElseGet(() -> ResponseEntity.status(HttpStatus.NOT_FOUND).body(null));

        } catch (Exception e) {
            log.error("Error al finalizar la prueba: ", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }

    // Endpoint para obtener los numeros de telefono de los empleados
    @GetMapping("/nros-telefono")
    public ResponseEntity<List<String>> obtenerNrosTelefono() {
        try {
            List<String> numeros = pruebaService.obtenerNrosTelefono();

            if (numeros.isEmpty()) {
                return ResponseEntity.noContent().build(); // 204 No Content
            }

            return ResponseEntity.ok(numeros); // 200 OK

        } catch (Exception e) {
            // En caso de error, registramos el error y devolvemos un 500 Internal Server Error
            log.error("Error al obtener los números de teléfono: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Collections.emptyList());
        }
    }

    // Endpoint para obtener el número de teléfono de un empleado por su legajo
    @GetMapping("/nro-telefono/{legajo}")
    public ResponseEntity<String> obtenerNroTelefono(@PathVariable Long legajo) {
        try {
            String telefono = pruebaService.obtenerNroTelefono(legajo);
            if (telefono == null || telefono.isEmpty()) {
                return ResponseEntity.notFound().build(); // Si no se encuentra el teléfono, 404 Not Found
            }

            return ResponseEntity.ok(telefono); // Devuelve el número de teléfono

        } catch (Exception e) {
            log.error("Error al obtener el número de teléfono para el legajo {}: {}", legajo, e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null); // Error interno del servidor
        }
    }
}