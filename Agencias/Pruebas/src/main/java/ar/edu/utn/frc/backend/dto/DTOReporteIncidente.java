package ar.edu.utn.frc.backend.dto;

import lombok.*;

import java.time.LocalDateTime;

@Data
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor

public class DTOReporteIncidente {

    private String patente;
    private String interesadoNombre;
    private String interesadoApellido;
    private String nombreEmpleado;
    private String apellidoEmpleado;
    private LocalDateTime fechaHoraIncidente;
    private String descripcionIncidente;
}