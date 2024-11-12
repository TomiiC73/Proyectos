package ar.edu.utn.frc.backend.controllers;

import ar.edu.utn.frc.backend.dto.DTOReporteDetallePruebaVehiculo;
import ar.edu.utn.frc.backend.dto.DTOReporteIncidente;
import ar.edu.utn.frc.backend.dto.DTOReporteIncidenteEmpleado;
import ar.edu.utn.frc.backend.dto.DTOReporteKilometrosRecorridos;
import ar.edu.utn.frc.backend.services.ReporteService;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Collections;
import java.util.List;

@RestController
@RequestMapping("/api/reportes")
public class ReportesController {

    private final ReporteService reporteService;

    @Autowired
    public ReportesController(ReporteService reporteService) {
        this.reporteService = reporteService;
    }

    // Endpoint para obtener el reporte de incidentes
    @GetMapping("/incidentes")
    public ResponseEntity<List<DTOReporteIncidente>> obtenerIncidentes() {
        List<DTOReporteIncidente> incidentes = reporteService.obtenerTodosLosIncidentes();
        return ResponseEntity.ok(incidentes);
    }

    @GetMapping("/empleado")
    public ResponseEntity<List<DTOReporteIncidenteEmpleado>> obtenerIncidentesPorEmpleado(
            @RequestParam String nombreEmpleado,
            @RequestParam String apellidoEmpleado) {

        List<DTOReporteIncidenteEmpleado> incidentes = reporteService.obtenerIncidentesPorEmpleado(nombreEmpleado, apellidoEmpleado);
        return ResponseEntity.ok(incidentes);
    }

    @GetMapping("/distancia")
    public ResponseEntity<String> obtenerKmRecorrido(@RequestBody DTOReporteKilometrosRecorridos dto) {
        try {
            Double distanciaTotal = reporteService.obtenerKmRecorridoDeVehiculo(dto);

            if (distanciaTotal > 0) {
                return ResponseEntity.ok("Cantidad de Km recorridos por el vehículo con patente " + dto.getPatente() + ": "
                        + distanciaTotal + " Km");
            } else {
                return ResponseEntity.ok("El vehículo ingresado no tiene km recorridos en el rango de fechas indicado...");
            }

        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body("Error: " + e.getMessage());

        } catch (Exception e) {
            return ResponseEntity.status(500).body("Error interno del servidor.");
        }
    }

    // Endpoint para obtener el detalle de las pruebas realizadas por vehículo
    @GetMapping("/detalle-pruebas/{idVehiculo}")
    public ResponseEntity<?> obtenerDetalleDePruebas(@PathVariable Long idVehiculo) {
        try {
            List<DTOReporteDetallePruebaVehiculo> reportePruebas = reporteService.obtenerDetalleDePruebasPorVehiculo(idVehiculo);

            // Si no hay pruebas, respondemos con una lista vacía (HTTP 200)
            if (reportePruebas.isEmpty()) {
                return ResponseEntity.ok().body(Collections.emptyList());
            }

            // Si hay pruebas, respondemos con la lista de detalles (HTTP 200)
            return ResponseEntity.ok(reportePruebas);

        } catch (EntityNotFoundException e) {
            // Si no se encuentra el recurso, respondemos con un 404 y un mensaje descriptivo
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("No se encontraron pruebas para el vehículo con ID: " + idVehiculo);

        } catch (Exception e) {
            // Para otros errores, respondemos con un 500 (Internal Server Error)
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body("Hubo un error al procesar la solicitud: " + e.getMessage());
        }
    }
}
