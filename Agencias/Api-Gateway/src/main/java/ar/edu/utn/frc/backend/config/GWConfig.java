package ar.edu.utn.frc.backend.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.cloud.gateway.route.RouteLocator;

@Configuration
public class GWConfig {

    @Bean
    public RouteLocator configurarRutas(RouteLocatorBuilder builder,
                                        @Value("${tpintegrador.url-microservicio-pruebas}") String uriPruebas,
                                        @Value("${tpintegrador.url-microservicio-notificaciones}") String uriNotificaciones) {

        return builder.routes()
                // Ruteo al microservicio pruebas
                .route(p -> p.path("/api/pruebas/**").uri(uriPruebas))

                // Ruteo al microservicio notificaciones
                .route(p -> p.path("/api/notificaciones/**").uri(uriNotificaciones))

                // Ruteo al microservicio posiciones
                .route(p -> p.path("/api/posiciones/**").uri(uriPruebas))

                // Ruteo al microservicio reportes
                .route(p -> p.path("/api/reportes/**").uri(uriPruebas))

                // Ruteo para desloguearse
                .route((p -> p.path("/api/logout").uri(uriPruebas)))
                .build();
    }
}