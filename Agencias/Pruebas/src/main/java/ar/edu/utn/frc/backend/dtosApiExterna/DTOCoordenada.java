package ar.edu.utn.frc.backend.dtosApiExterna;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

@Data
@AllArgsConstructor
@NoArgsConstructor

public class DTOCoordenada {

    @JsonProperty("lat")
    private Double latitud;

    @JsonProperty("lon")
    private Double longitud;
}
