package ar.edu.utn.frc.backend.distancias;

import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor

public class Area {

    Coordenada noroeste;
    Coordenada sureste;

    public boolean contiene(Coordenada punto) {

        return punto.getLatitud() <= noroeste.getLatitud() && punto.getLatitud() >= sureste.getLatitud() &&
                punto.getLongitud() >= noroeste.getLongitud() && punto.getLongitud() <= sureste.getLongitud();
    }
}
