$(function () {
    // Configuración para elementos con la clase 'select2'
    $('.select2').select2({
      theme: 'bootstrap4',
      language: 'es'
    });
  
    // Configuración para el campo de entrada con el atributo 'name' igual a 'pvp'
    $('input[name="pvp"]').TouchSpin({
      min: 0.01,
      max: 1000000,
      step: 0.01,
      decimals: 2,
      boostat: 5,
      verticalbuttons: true,
      maxboostedstep: 10,
      prefix: ''
    }).on('keypress', function (e) {
      return validate_decimals($(this), e);
    });
  
    // Configuración para el campo de entrada con el atributo 'name' igual a 'stock'
    $('input[name="stock"]').TouchSpin({
      min: 0,
      max: 1000000,
      step: 1,
      verticalbuttons: true
    }).on('keypress', function (e) {
      return validate_form_text('numbers', e, null);
    });
  });