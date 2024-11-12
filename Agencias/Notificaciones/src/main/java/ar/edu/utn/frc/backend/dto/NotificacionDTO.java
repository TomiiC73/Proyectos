package ar.edu.utn.frc.backend.dto;

import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class NotificacionDTO {

    private String mensaje;
    private Long legajo;
}
