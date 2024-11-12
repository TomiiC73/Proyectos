package ar.edu.utn.frc.backend.controllers;

import ar.edu.utn.frc.backend.dtosApiExterna.DTOPosicionAPI;
import ar.edu.utn.frc.backend.services.APIExternaService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@Slf4j
@RestController
@RequestMapping("/posiciones")
public class ConfiguracionAPIController {

    @Autowired
    private APIExternaService myService;

    @GetMapping("/configuracion")
    public ResponseEntity<DTOPosicionAPI> getPosicionAPI() {
        DTOPosicionAPI configuracion = myService.getConfiguracionAPI();
        return ResponseEntity.ok(configuracion);
    }
}
