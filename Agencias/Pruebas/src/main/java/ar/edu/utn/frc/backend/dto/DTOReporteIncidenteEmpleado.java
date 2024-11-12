package ar.edu.utn.frc.backend.dto;

import lombok.*;

import java.time.LocalDateTime;

@Data
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor

public class DTOReporteIncidenteEmpleado {

    private String patente;
    private String nombreEmpleado;
    private String apellidoEmpleado;
    private String interesadoNombre;
    private String interesadoApellido;
    private LocalDateTime fechaHoraIncidente;
    private String descripcionIncidente;
}