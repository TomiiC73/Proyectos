package ar.edu.utn.frc.backend.dtosApiExterna;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonRootName;
import lombok.*;

@Data
@AllArgsConstructor
@NoArgsConstructor

@JsonRootName(value = "zonasRestringidas")
public class DTOZonaRestringida {

    @JsonProperty("noroeste")
    private DTOCoordenada noroeste;

    @JsonProperty("sureste")
    private DTOCoordenada sureste;
}
