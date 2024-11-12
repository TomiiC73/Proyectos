package ar.edu.utn.frc.backend.dto;

import lombok.*;

@Data
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor

public class DTOPruebaEnCurso {

    private String patente;
    private String nombreInteresado;
    private String apellidoInteresado;
    private String nombreEmpleado;
    private String apellidoEmpleado;
    private String fechaHoraInicio;
}
