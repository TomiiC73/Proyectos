package ar.edu.utn.frc.backend.dto;

import lombok.*;

@Data
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor

public class DTOReporteDetallePruebaVehiculo {

    private Long pruebaId;
    private String patente;
    private String nombreInteresado;
    private String apellidoInteresado;
    private String nombreEmpleado;
    private String apellidoEmpleado;
    private String fechaHoraInicio;
    private String fechaHoraFin;
    private String comentarios;
}