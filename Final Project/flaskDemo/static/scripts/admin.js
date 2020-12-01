
function changeManagmentContent(model) {
console.log(model);

$("#manageTitle").text(model);

$.ajax({
    method: 'GET',
    url: "/admin/manage",
    data: {'model':model},
    success: function(response) {
        console.log(response);
        fillTable(response);
    }
})


}

function fillTable(array) {
    var html = '';
    for (var i = 0; i <array.length; i++) {
        html += '<tr><td>' + '<span class="custom-checkbox">'+ 
        '<input type="checkbox" id="checkbox1" name="options[]" value="1">' +
        '<label for="checkbox1"></label> </span>' +'</td><td>' + array[i].FName + ' ' + array[i].LName + '</td><td>' +
        array[i].Email + '</td><td>' + array[i].UserType + '</td><td>' + array[i].PhoneNum + '</td><td>'
        + '<a href="#editEmployeeModal" class="edit" data-toggle="modal"><i class="material-icons"' +
        'data-toggle="tooltip" title="Edit">&#xE254;</i></a>' +
        '<a href="#deleteEmployeeModal" class="delete" data-toggle="modal"><i class="material-icons"' +
        'data-toggle="tooltip" title="Delete">&#xE872;</i></a>' + '</td></tr>';

    }
    $('#table tr').first().after(html);
}