package ar.edu.utn.frc.backend.dto;

import lombok.*;
import org.springframework.context.annotation.Configuration;

import java.time.LocalDateTime;

@Data
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Configuration
public class DTOReporteKilometrosRecorridos {

    private String patente;
    private String fechaHoraInicio;
    private String fechaHoraFin;
}
