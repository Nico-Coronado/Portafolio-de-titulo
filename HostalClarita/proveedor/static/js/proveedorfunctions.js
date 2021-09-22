$(document).ready( function () {

    
//Tabla de productos de proveedor:
$('#tablaProduProv').DataTable({       
    language: {
        url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
    },
    dom: 'Bfrtip',
    buttons: [
        { 
            extend: 'copy',
            exportOptions: {
            columns: [ 0, 1, 2,3,4,5,6,7,8 ]
        }},
        { 
            extend: 'csv',
            exportOptions: {
            columns: [ 0, 1, 2,3,4,5,6,7,8 ]
        } },
        { 
            extend: 'excel',
            exportOptions: {
            columns: [ 0, 1, 2,3,4,5,6,7,8 ]
        } },
        { 
            extend: 'pdf',
            exportOptions: {
            columns: [ 0, 1, 2,3,4,5,6,7,8 ]
        } },
        { 
            extend: 'print',
            exportOptions: {
            columns: [ 0, 1, 2,3,4,5,6,7,8 ]
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

$('#tablaPedidosPendi').DataTable({       
    language: {
        url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
    },
    dom: 'Bfrtip',
    buttons: [
        { 
            extend: 'copy',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        }},
        { 
            extend: 'csv',
            exportOptions: {
            columns: [ 0, 1, 2]
        } },
        { 
            extend: 'excel',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } },
        { 
            extend: 'pdf',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } },
        { 
            extend: 'print',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } 
    }
    ],
    initComplete: function () {
        var btns = $('.dt-button');
        btns.addClass('btn btn-info btn-sm');
        btns.removeClass('dt-button');
    }

});   


$('#tablaHistorialA').DataTable({       
    language: {
        url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
    },
    dom: 'Bfrtip',
    buttons: [
        { 
            extend: 'copy',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        }},
        { 
            extend: 'csv',
            exportOptions: {
            columns: [ 0, 1, 2]
        } },
        { 
            extend: 'excel',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } },
        { 
            extend: 'pdf',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } },
        { 
            extend: 'print',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } 
    }
    ],
    initComplete: function () {
        var btns = $('.dt-button');
        btns.addClass('btn btn-info btn-sm');
        btns.removeClass('dt-button');
    }

});   

$('#tablaHistorialE').DataTable({       
    language: {
        url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
    },
    dom: 'Bfrtip',
    buttons: [
        { 
            extend: 'copy',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        }},
        { 
            extend: 'csv',
            exportOptions: {
            columns: [ 0, 1, 2]
        } },
        { 
            extend: 'excel',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } },
        { 
            extend: 'pdf',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } },
        { 
            extend: 'print',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } 
    }
    ],
    initComplete: function () {
        var btns = $('.dt-button');
        btns.addClass('btn btn-info btn-sm');
        btns.removeClass('dt-button');
    }

});   

$('#tablaHistorialC').DataTable({       
    language: {
        url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
    },
    dom: 'Bfrtip',
    buttons: [
        { 
            extend: 'copy',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        }},
        { 
            extend: 'csv',
            exportOptions: {
            columns: [ 0, 1, 2]
        } },
        { 
            extend: 'excel',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } },
        { 
            extend: 'pdf',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } },
        { 
            extend: 'print',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } 
    }
    ],
    initComplete: function () {
        var btns = $('.dt-button');
        btns.addClass('btn btn-info btn-sm');
        btns.removeClass('dt-button');
    }

});   

$('#tablaHistorialR').DataTable({       
    language: {
        url: 'https://cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
    },
    dom: 'Bfrtip',
    buttons: [
        { 
            extend: 'copy',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        }},
        { 
            extend: 'csv',
            exportOptions: {
            columns: [ 0, 1, 2]
        } },
        { 
            extend: 'excel',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } },
        { 
            extend: 'pdf',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } },
        { 
            extend: 'print',
            exportOptions: {
            columns: [ 0, 1, 2 ]
        } 
    }
    ],
    initComplete: function () {
        var btns = $('.dt-button');
        btns.addClass('btn btn-info btn-sm');
        btns.removeClass('dt-button');
    }

});   

$("#id_precio").on("change", function(){

    if($("#id_precio").val() < 0){
        alert("el precio del producto no puede ser negativo.");
        $("#id_precio").val(0);

    }

});


$("#id_stock").on("change", function(){

    if($("#id_stock").val() < 0){
        alert("el stock del producto no puede ser negativo.");
        $("#id_stock").val(0);

    }

});


$("#id_stock_critico").on("change", function(){

    if($("#id_stock_critico").val() < 0){
        alert("el stock critico del producto no puede ser negativo.");
        $("#id_stock_critico").val(0);

    }

});



});


