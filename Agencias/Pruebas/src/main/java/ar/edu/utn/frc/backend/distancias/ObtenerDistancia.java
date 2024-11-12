package ar.edu.utn.frc.backend.distancias;

import lombok.*;
import org.springframework.context.annotation.Configuration;

@Data
@NoArgsConstructor
@Configuration
public class ObtenerDistancia {

    private static final Double radioTierra = 6371.0; // Radio de la Tierra en kilómetros

    public static Double calcularDistancia(Coordenada coord1, Coordenada coord2) {

        double latDistance = Math.toRadians(coord2.getLatitud() - coord1.getLatitud());
        double lonDistance = Math.toRadians(coord2.getLongitud() - coord1.getLongitud());

        double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2)

                + Math.cos(Math.toRadians(coord1.getLatitud())) * Math.cos(Math.toRadians(coord2.getLatitud()))
                * Math.sin(lonDistance / 2) * Math.sin(lonDistance / 2);

        Double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return radioTierra * c; // Distancia en kilómetros
    }
}