package ar.edu.utn.frc.backend.controllers;

import ar.edu.utn.frc.backend.dto.NotificacionDTO;
import ar.edu.utn.frc.backend.dto.NotificacionPromocionDTO;
import ar.edu.utn.frc.backend.services.NotificacionService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
@RequestMapping("/api/notificaciones")
public class NotificacionController {

    @Autowired
    private NotificacionService notificacionService;

    @GetMapping("/saludo")
    public ResponseEntity<String> test() {
        return ResponseEntity.ok("Hola!");
    }

    // Enpoint para crear una notificacion de zona restringida o fuera del radio de la agencia
    @PostMapping("/crear")
    public ResponseEntity<String> crearNotificacion(@RequestBody NotificacionDTO notificacionDTO) {
        try {
            notificacionService.crearNotificacion(notificacionDTO.getMensaje(), notificacionDTO.getLegajo());
            return ResponseEntity.ok("Notificacion enviada!");

        } catch (Exception e) {
            log.error("Error al crear la notificacion: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }

    // Endpoint para crear una notificacion de promocion
    @PostMapping("/crear-promocion")
    public ResponseEntity<String> crearNotificacionesDePromocion(@RequestBody NotificacionPromocionDTO notificacionPromocionDTO) {
        if (notificacionPromocionDTO.getMensaje() == null || notificacionPromocionDTO.getMensaje().trim().isEmpty()) {

            log.warn("Mensaje de promoción no proporcionado.");
            return ResponseEntity.badRequest().body("El mensaje de promoción no puede estar vacío.");
        }

        try {
            notificacionService.enviarNotificacionPromocion(notificacionPromocionDTO.getMensaje());
            return ResponseEntity.ok("Notificaciones de promoción enviadas correctamente.");

        } catch (Exception e) {
            log.error("Error al crear notificaciones de promoción: ", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error al enviar las notificaciones de promoción.");
        }
    }
}
