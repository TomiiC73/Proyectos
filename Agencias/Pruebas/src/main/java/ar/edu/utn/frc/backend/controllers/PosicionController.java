package ar.edu.utn.frc.backend.controllers;

import ar.edu.utn.frc.backend.dto.DTOActualizarPosicion;
import ar.edu.utn.frc.backend.dto.DTOPosicionVehiculo;
import ar.edu.utn.frc.backend.dtosApiExterna.DTOPosicionAPI;
import ar.edu.utn.frc.backend.entities.Posicion;
import ar.edu.utn.frc.backend.entities.Vehiculo;
import ar.edu.utn.frc.backend.repositorios.PosicionRepositorio;
import ar.edu.utn.frc.backend.repositorios.VehiculoRepositorio;
import ar.edu.utn.frc.backend.services.PosicionService;
import jakarta.persistence.EntityNotFoundException;
import lombok.extern.slf4j.Slf4j;
import org.hibernate.service.spi.ServiceException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@Slf4j
@RestController
@RequestMapping("/api/posiciones")

public class PosicionController {

    private final PosicionService posicionService;
    private final PosicionRepositorio posicionRepositorio;
    private final VehiculoRepositorio vehiculoRepositorio;

    @Autowired
    public PosicionController(PosicionService posicionService, PosicionRepositorio posicionRepositorio, VehiculoRepositorio vehiculoRepositorio) {
        this.posicionService = posicionService;
        this.posicionRepositorio = posicionRepositorio;
        this.vehiculoRepositorio = vehiculoRepositorio;
    }

    // Endpoint para verificar si un punto esta dentro de las coordenadas
    @PostMapping("/verificar")
    public ResponseEntity<Boolean> verificarPunto(@RequestBody DTOPosicionVehiculo dtoPosicionVehiculo) {
        try {
            boolean estaDentro;
            // Cargamos las zonas de la api a los DTOs
            DTOPosicionAPI dtoPosicionAPI = posicionService.cargarZonasDesdeAPI();

            // Buscamos el id del vehiculo asociado a la patente ingresada
            Long vehiculoId = vehiculoRepositorio.findIdByPatente(dtoPosicionVehiculo.getPatente());
            Optional<Vehiculo> vehiculo = vehiculoRepositorio.findById(vehiculoId);

            // Buscamos la posicion asociada al id del vehiculo
            Posicion posicion = posicionRepositorio.findFirstByVehiculoOrderByFechaHoraDesc(vehiculo);

            if (posicion == null) {
                log.error("No se encontró la posición para el vehículo con ID: {}", vehiculoId);
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(null);  // O el código adecuado
            }

            if (dtoPosicionAPI != null) {
                estaDentro = posicionService.verificarPunto(posicion, dtoPosicionAPI, vehiculoId);
            } else {
                log.error("Datos inválidos: posición o datos de API no disponibles.");
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(null);
            }
            return ResponseEntity.ok(estaDentro);

        } catch (ServiceException e) {
            log.error("Error al verificar la posicion del vehiculo: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);

        } catch (Exception e) {
            log.error("Error inesperado: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }

    @PatchMapping("/agregar")
    public ResponseEntity<String> agregarPosicion(@RequestBody DTOActualizarPosicion dtoActualizarPosicion) {
        try {
            // Buscar el vehículo por patente
            Long vehiculoId = vehiculoRepositorio.findIdByPatente(dtoActualizarPosicion.getPatente());
            if (vehiculoId == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Vehículo no encontrado.");
            }

            // Buscar el vehículo en la bd
            Vehiculo vehiculo = vehiculoRepositorio.findById(vehiculoId)
                    .orElseThrow(() -> new EntityNotFoundException("Vehículo no encontrado para el ID: " + vehiculoId));

            // Llamar al servicio para agregar la nueva posición
            posicionService.agregarNuevaPosicion(vehiculo, dtoActualizarPosicion);

            return ResponseEntity.ok("Posición agregada correctamente!");

        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(e.getMessage());

        } catch (EntityNotFoundException e) {
            return ResponseEntity.status(404).body(e.getMessage());

        } catch (Exception e) {
            log.error("Error inesperado: {}", e.getMessage(), e);  // Esto te dará el stack trace completo
            return ResponseEntity.status(500).body("Error interno del servidor.");
        }
    }
}