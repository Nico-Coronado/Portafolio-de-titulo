$(document).ready( function () {
    //Tabla de Habitaciones
    $('#tablaHabi').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
            { 
                extend: 'copy',
                exportOptions: {
                columns: [ 0, 1, 2,3,4 ]
            }},
            { 
                extend: 'csv',
                exportOptions: {
                columns: [ 0, 1, 2,3,4 ]
            } },
            { 
                extend: 'excel',
                exportOptions: {
                columns: [ 0, 1, 2,3,4 ]
            } },
            { 
                extend: 'pdf',
                exportOptions: {
                columns: [ 0, 1, 2,3,4 ]
            } },
            { 
                extend: 'print',
                exportOptions: {
                columns: [ 0, 1, 2,3,4 ]
            } 
        }
        ],
        initComplete: function () {
            var btns = $('.dt-button');
            btns.addClass('btn btn-info btn-sm');
            btns.removeClass('dt-button');
        },
        pageLength: 5,

 
    });
//Tabla de huéspedes.

$('#tablaHuesped').DataTable({
    language: {
        url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
    },
    dom: 'Bfrtip',
    buttons: [
        'copy', 'csv', 'excel', 'pdf', 'print'
    ],
    initComplete: function () {
        var btns = $('.dt-button');
        btns.addClass('btn btn-primary btn-sm');
        btns.removeClass('dt-button');
    }

});


//Tablas de factura

    $('#tablaFactura').DataTable({
       
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
            { 
                extend: 'copy',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            }},
            { 
                extend: 'csv',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } },
            { 
                extend: 'excel',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } },
            { 
                extend: 'pdf',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } },
            { 
                extend: 'print',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } 
        }
        ],
        initComplete: function () {
            var btns = $('.dt-button');
            btns.addClass('btn btn-success btn-sm');
            btns.removeClass('dt-button');
        }
 
    });

    //Tabla de platos:
    $('#tablaPlato').DataTable({
       
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
            { 
                extend: 'copy',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            }},
            { 
                extend: 'csv',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } },
            { 
                extend: 'excel',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } },
            { 
                extend: 'pdf',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } },
            { 
                extend: 'print',
                exportOptions: {
                columns: [ 0, 1, 2,3,4,5 ]
            } 
        }
        ],
        initComplete: function () {
            var btns = $('.dt-button');
            btns.addClass('btn btn-primary btn-sm');
            btns.removeClass('dt-button');
        }
 
    });


    //Tabla de pedidos:
    $('#tablaPedidos').DataTable({
       
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
        },
        dom: 'Bfrtip',
        buttons: [
            { 
                extend: 'copy',
                exportOptions: {
                columns: [ 0, 1, 2,3],
            }},
            { 
                extend: 'csv',
                exportOptions: {
                columns: [ 0, 1, 2,3]
            } },
            { 
                extend: 'excel',
                exportOptions: {
                columns: [ 0, 1, 2,3]
            } },
            { 
                extend: 'pdf',
                exportOptions: {
                columns: [ 0, 1, 2,3]
            } },
            { 
                extend: 'print',
                exportOptions: {
                columns: [ 0, 1, 2,3]
            } 
        }
        ],
        initComplete: function () {
            var btns = $('.dt-button');
            btns.addClass('btn btn-warning btn-sm');
            btns.removeClass('dt-button');
        }
 
    });

//Tabla de ganancias
 
$('#tablaGanancias').DataTable({
    language: {
        url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
    },
    dom: 'Bfrtip',
    buttons: [
        'copy', 'csv', 'excel', 'pdf', 'print'
    ],
    initComplete: function () {
        var btns = $('.dt-button');
        btns.addClass('btn btn-success btn-sm');
        btns.removeClass('dt-button');
    }

});



//Tabla de productos
 
$('#tablaTodoProdus').DataTable({
    language: {
        url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
    },
    dom: 'Bfrtip',
    buttons: [
        'copy', 'csv', 'excel', 'pdf', 'print'
    ],
    initComplete: function () {
        var btns = $('.dt-button');
        btns.addClass('btn btn-success btn-sm');
        btns.removeClass('dt-button');
    }

});

//Tabla de gastos

$('#tablaGastos').DataTable({
    language: {
        url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
    },
    dom: 'Bfrtip',
    buttons: [
        'copy', 'csv', 'excel', 'pdf', 'print'
    ],
    initComplete: function () {
        var btns = $('.dt-button');
        btns.addClass('btn btn-info btn-sm');
        btns.removeClass('dt-button');
    }

});
 


//Tabla de visitas

$('#tablaVisitas').DataTable({
    language: {
        url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
    },
    dom: 'Bfrtip',
    buttons: [
        'copy', 'csv', 'excel', 'pdf', 'print'
    ],
    initComplete: function () {
        var btns = $('.dt-button');
        btns.addClass('btn btn-warning btn-sm');
        btns.removeClass('dt-button');
    }

});

//Validaciones lado del cliente.
$("#id_numero_de_habitacion").on("change", function(){

    if($("#id_numero_de_habitacion").val() < 0){
        alert("El número de la habitación no puede ser negativo.");
        $("#id_numero_de_habitacion").val(0);

    }
    

});

$("#id_precio").on("change", function(){

    if($("#id_precio").val() < 0){
        alert("El precio de la habitación no puede ser negativo.");
        $("#id_precio").val(0);
    }

});


$("#id_idcomedor").on("change", function(){

    if($("#id_idcomedor").val() < 0){
        alert("la id del comedor no puede ser negativa.");
        $("#id_idcomedor").val(0);
    }

});

$("#id_idcomedore").on("change", function(){

    if($("#id_idcomedore").val() < 0){
        alert("la id del comedor no puede ser negativa.");
        $("#id_idcomedore").val(0);

    }

});

$("#id_idcomedora").on("change", function(){

    if($("#id_idcomedora").val() < 0){
        alert("la id del comedor no puede ser negativa.");
        $("#id_idcomedora").val(0);

    }

});

$("#id_precio_plato").on("change", function(){

    if($("#id_precio_plato").val() < 0){
        alert("el precio del plato no puede ser negativo.");
        $("#id_precio_plato").val(0);

    }

});

$("#id_valor_peso").on("change", function(){

    if($("#id_valor_peso").val() < 0){
        alert("el valor del peso no puede ser negativo.");
        $("#id_valor_peso").val(0);

    }

});

$("#id_valor_pesoa").on("change", function(){

    if($("#id_valor_pesoa").val() < 0){
        alert("el valor del peso no puede ser negativo.");
        $("#id_valor_pesoa").val(0);

    }

});



} );