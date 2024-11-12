package ar.edu.utn.frc.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DTONotificacion {

    private String mensaje;
    private Long legajo;
}
