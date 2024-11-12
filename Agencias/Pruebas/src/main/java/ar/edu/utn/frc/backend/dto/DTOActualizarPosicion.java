package ar.edu.utn.frc.backend.dto;

import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DTOActualizarPosicion {

    private String patente;
    private Double latitud;
    private Double longitud;
}
