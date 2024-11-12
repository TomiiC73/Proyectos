package ar.edu.utn.frc.backend.dto;

import lombok.Data;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor

public class DTOCrearPrueba {

    private Long vehiculoId;
    private Long interesadoId;
    private Long empleadoId;
}
