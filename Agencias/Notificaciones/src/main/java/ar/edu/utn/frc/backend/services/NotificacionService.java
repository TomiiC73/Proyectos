package ar.edu.utn.frc.backend.services;

import ar.edu.utn.frc.backend.entities.Notificacion;
import ar.edu.utn.frc.backend.repositories.NotificacionRepositorio;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Collections;
import java.util.List;

@Slf4j
@Service
public class NotificacionService {

    private final NotificacionRepositorio notificacionRepositorio;
    private final RestTemplate restTemplate;
    private DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    // URL del microservicio de Pruebas para obtener los números de teléfono
    private static final String PRUEBAS_URL = "http://localhost:8082/api/pruebas";

    @Autowired
    public NotificacionService(NotificacionRepositorio notificacionRepositorio, RestTemplate restTemplate) {
        this.notificacionRepositorio = notificacionRepositorio;
        this.restTemplate = restTemplate;
    }

    public void crearNotificacion(String mensaje, Long legajo) {
        LocalDateTime fechaHora = LocalDateTime.now();
        String fechaHoraFormateada = fechaHora.format(formatter);

        String nroTelefono = obtenerNroTelefono(legajo);

        Notificacion notificacion = new Notificacion();
        notificacion.setMensaje(mensaje);
        notificacion.setFechaHoraEnvio(fechaHoraFormateada);
        notificacion.setNroTelefono(nroTelefono);

        notificacionRepositorio.save(notificacion);

        log.info("Notificación creada: " + mensaje + " para el número: " + nroTelefono);
    }

    // Metodo para obtener el número de telefono, de acuerdo con el tipo de endpoint
    private String obtenerNroTelefono(Long legajo) {
        try {
            String url = PRUEBAS_URL + "/nro-telefono/" + legajo;
            return restTemplate.getForObject(url, String.class);
        } catch (Exception e) {
            log.error("Error al obtener el número de teléfono para el legajo de empleado: " + legajo, e);
            return "Número no disponible";
        }
    }

    private List<String> obtenerNrosTelefonos() {
        try {
            String url = PRUEBAS_URL + "/nros-telefono";

            ResponseEntity<List<String>> response = restTemplate.exchange(
                    url,
                    HttpMethod.GET,
                    null,
                    new ParameterizedTypeReference<List<String>>() {}
            );

            // Retornamos la lista de números de teléfono
            return response.getBody();

        } catch (Exception e) {
            log.error("Error al obtener los números de teléfono: ", e);
            return Collections.emptyList();
        }
    }

    public void enviarNotificacionPromocion(String mensaje) {
        LocalDateTime fechaHora = LocalDateTime.now();
        String fechaHoraFormateada = fechaHora.format(formatter);

        // Obtener la lista de números de teléfono
        List<String> numeros = this.obtenerNrosTelefonos();

        // Si no hay números, no es necesario continuar
        if (numeros.isEmpty()) {
            log.warn("No se encontraron números de teléfono para enviar la promoción.");
            return;
        }

        // Iniciar el conteo de notificaciones enviadas
        int notificacionesEnviadas = 0;
        int notificacionesFallidas = 0;

        for (String telefono : numeros) {
            try {
                Notificacion notificacion = new Notificacion();
                notificacion.setMensaje(mensaje);
                notificacion.setFechaHoraEnvio(fechaHoraFormateada);
                notificacion.setNroTelefono(telefono);

                // Guardar la notificación
                notificacionRepositorio.save(notificacion);
                notificacionesEnviadas++;

            } catch (Exception e) {
                log.error("Error al guardar la notificación para el número: {}", telefono, e);
                notificacionesFallidas++;
            }
        }
        log.info("Notificaciones procesadas: {} enviadas correctamente, {} fallidas.", notificacionesEnviadas, notificacionesFallidas);
    }
}