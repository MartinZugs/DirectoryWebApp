
function changeManagmentContent(model) {
    console.log(model);

    $("#manageTitle").text(model);
    
    changeModalOptions(model);

    var table = document.getElementById('table');
    var rowCount = table.rows.length;
    if (rowCount > 1) {
    for (var i = 1; i < rowCount; i++) {
        table.deleteRow(1);
        if (i == rowCount-1) {
            getModel(model);
        }
    }
} else {
    getModel(model);
}




}

function changeModalOptions(model) {
    //edit addmodal
    if (model == 'All') {
        $("#addTitle").text('Person');
        $("#modaladdItemTitle").text('Person');
        $("#modaldeleteItemTitle").text('Person');
        $("#modaleditItemTitle").text('Person');
        getModelDetails(model, changeModalCallback);
    } else {
        $("#addTitle").text(model);
        $('#modaladdItemTitle').text(model);
        $("#modaldeleteItemTitle").text(model);
        $("#modaleditItemTitle").text(model);
        getModelDetails(model, changeModalCallback);
    }
    
}

function addInput(detail, value) {
    //console.log(detail, value);
    var div = document.createElement('div');
    div.className = 'form-group row'

    
    if (value == null) {
        var label = document.createElement('label');
        label.innerHTML = detail;
        label.className = 'col-sm-3 col-form-label';
        div.append(label);
        var inputDiv = document.createElement('div');
        inputDiv.className = "col-sm-9";

        var i = document.createElement("input");
        i.type = "text";
        i.name = detail;
        i.className = "form-control";
        i.required = true
        
        inputDiv.append(i);
        div.append(inputDiv);
    } else if (value == "bool") {
        var label = document.createElement('div');
        label.innerHTML = detail;
        label.className = "col-sm-3";
        div.append(label);

        var checkDiv = document.createElement('div');
        checkDiv.className = "form-check"

        var innerDiv = document.createElement('div');
        checkDiv.className = "col-sm-9"

        var i = document.createElement("input");
        i.type = "checkbox";
        i.name = detail;
        i.className = "form-check-input custom-checkbox";
        

        checkDiv.append(i);
        innerDiv.append(checkDiv);
        div.append(innerDiv);

    } else if (Array.isArray(value)) {
        var label = document.createElement('label');
        label.innerHTML = detail;
        label.className = 'col-sm-3 col-form-label';
        div.append(label);
        var inputDiv = document.createElement('div');
        inputDiv.className = "col-sm-9";

        //var label = document.createElement('label');
        //label.innerHTML = detail;
        //div.append(label);
        var i = document.createElement("select");
        i.className = "form-control";
        i.name = detail;
        i.required = true
        for (let option of value) {
            let opt = createOption(detail, option);
            i.append(opt);
        }
        inputDiv.append(i);
        div.append(inputDiv);
    }
    //i.id = "user_name1";
    

    return div;
}

function createOption(detail, option) {
    var opt = document.createElement("option");
    //console.log(detail, option);
    switch (detail) {
        case "PersonID":
            opt.value = option.PersonID;
            opt.text  = option.FName + ' ' + option.LName;
            break;
        case "ManagerID":
            if (option.EmployeeID == null) {
                opt.value = '';
                opt.text = "None";
            } else {
                opt.value = option.EmployeeID;
                opt.text  = option.FName + ' ' + option.LName;
            }
            break;
        case "CampusID":
            opt.value = option.CampusID;
            opt.text  = option.CampusName
            break;
        case "BuildingID":
            opt.value = option.BuildingID;
            opt.text = option.BuildingName;
            break;
        case "EmployeeID":
            if (option.EmployeeID == null) {
                opt.value = '';
                opt.text = "None";
            } else {
                opt.value = option.EmployeeID;
                opt.text = option.FName + ' ' + option.LName;
            }
            break;
        case "OfficeID":
            if (option.OfficeID == null) {
                opt.value = '';
                opt.text = "None"
            } else {
                opt.value = option.OfficeID;
                opt.text = option.BuildingName + ' Room ' + option.OfficeID;
            }
            break;
        case "DepartmentID":
            opt.value = option.DepartmentID;
            opt.text = option.DepartmentName;
            break;
        case "ProfID":
            if (option.EmployeeID == null) {
                opt.value = null;
                opt.text = "None";
            } else {
                opt.value = option.EmployeeID;
                opt.text = option.FName + ' ' + option.LName;
            }
            break;
        case "MainCourseID":
            opt.value = option.CourseID;
            opt.text = option.CourseDescription //might be switched to CourseName //todo
            break;
        case "PrereqID":
            opt.value = option.CourseID;
            opt.text = option.CourseDescription //might be switched to CourseName //todo
            break;
        case "CourseID":
            opt.value = option.CourseID;
            opt.text = option.CourseDescription //might be switched to CourseName //todo
            break;
        case "StudentID":
            opt.value = option.StudentID;
            opt.text = option.FName + ' ' + option.LName;
            break;
        default:
            opt.value = option.type;
            opt.text  = option.type;
            break;
    }

    return opt;
}



function addForm(details, model, modalName) {
    //console.log(modalName + "Form");
    var f = document.getElementById(modalName + "Form");
    f.setAttribute('model', model);
    //console.log(f);
    //f.setAttribute('method', "post");
    
    
    var body = document.createElement('div');
    body.className = "modal-body";
    f.append(body);
    //f.id = 
    //create input element
    for (let key in details) {
        var div = addInput(key, details[key]);
        body.appendChild(div);
    }
        
    var footer = document.createElement('div');
    footer.className = "modal-footer";
    
    //create a button
    var s = document.createElement("input");
    s.type = "submit";
    s.value = "Save";
    s.className = "btn btn-primary";

    var close = document.createElement("button");
    close.className = 'btn btn-secondary';
    close.setAttribute("data-dismiss", "modal");
    close.innerHTML = "Close";
    footer.append(close);
    footer.append(s);

    f.append(footer);
    // add all elements to the form
    //f.appendChild(div);
    //f.appendChild(s);

    // add the form inside the body
    //$(modalName).append(f);
    
    
}

//function changeModalFields(model) {
//    switch (model) {
//        case 'Student':

//            getModelDetails(model, changeModalCallback);
//            //console.log(modelDetails);
//            break;
//        case 'All':

//            getModelDetails(model, changeModalCallback);
//            break;
//    }

    
//}

function changeModalCallback(details, model) {
    //console.log(details)
    //remove contents from modals
    $('#addModalContentForm').empty();
    $('#editModalContentForm').empty();

    //populate modals with the details
    addForm(details, model, 'addModalContent');
    addForm(details, model, 'editModalContent');
}

function getModelDetails(model, callback) {
    $.ajax({
        method: 'GET',
        url: "/admin/modelDetails",
        data: { 'model': model },
        success: function (response) {
            //console.log(response)
            callback(response, model)
        }
    })
}


var currentTableEntries;

function getModel(model){
    $.ajax({
        method: 'GET',
        url: "/admin/manage",
        data: {'model':model},
        success: function (response) {
            currentTableEntries = response;
            //console.log(response);
            fillTable(response);
        }
    })
}


function fillTable(array) {
    if (array != null) {
        $("#amountOfEntries").text(array.length);
        var html = '';
        for (var i = 0; i < array.length; i++) {
            html += '<tr elementid="' + array[i].MainCourseID + '" elementid2=' + array[i].PrereqID + '><td>' +
                '<input type="checkbox" id="checkbox'+i+'" name="options[]" value="1">' +
                '<label for="checkbox1"></label>' + '</td><td>' + array[i].FName + ' ' + array[i].LName + '</td><td>' +
                array[i].Email + '</td><td>' + array[i].UserType + '</td><td>' + array[i].PhoneNum + '</td><td>' +
                convertToBoolean(array[i].Manager) + '</td><td>'
                + '<a href="#editModal" class="edit" data-toggle="modal"><i class="material-icons"' +
                'data-toggle="tooltip" title="Edit" onclick="editRow(this);">&#xE254;</i></a>' +
                '<a class="delete" ><i class="material-icons"' +
                'data-toggle="tooltip" title="Delete" onclick="deleteRow(this);">&#xE872;</i></a>' + '</td></tr>';

        }
        $('#table tbody').append(html);
    }
    
}

function convertToBoolean(bit) {
    if (bit == 1) {
        return true;
    } else {
        return false;
    }
}



function addFormSubmit(e) {
    e.preventDefault();
    let model = $('#addModalContentForm').attr('model');
    let sendData = true;
    let errorMessage = '';
    console.log(model);
    data = { 'model': model }
    $.each($('#addModalContentForm').serializeArray(), function (i, field) {
       
        
        data[field.name] = field.value;
        
        
    });
    if (model == "All") {
        if (data['Manager'] == "on") {
            data['Manager'] = true;
        } else {
            data['Manager'] = false;
        }
    } else if (model == "Employee") {
        if (data['ManagerID'] == data['PersonID']) {
            sendData = false;
            errorMessage = "Cant be your own Manager";
        }
    } else if (model == "Prereqs") {
        if (data['PrereqID'] == data['MainCourseID']) {
            sendData = false;
            errorMessage = "A Course cant be its own Prereq";
        }
    }
    //switch (model) {
    //    case "All":
    //        $
    //        data['email'] = model 
    //        break;
    //}
    if (sendData) {
        sendAddFormData(data);
    }
    
    $("input[type=text], textarea").val("");
    $('#addModal').modal("hide");
}

function editFormSubmit(e) {
    e.preventDefault();
    let model = $('#editModalContentForm').attr('model');
    let sendData = true;
    let errorMessage = '';
    //console.log(model);
    data = { 'model': model, "id": $('#editModalContentForm').attr('elementid')}
    $.each($('#editModalContentForm').serializeArray(), function (i, field) {
        data[field.name] = field.value;
    });
    if (model == "All") {
        if (data['Manager'] == "on") {
            data['Manager'] = true;
        } else {
            data['Manager'] = false;
        }
    } else if (model == "Employee") {
        if (data['ManagerID'] == data['PersonID']) {
            sendData = false;
            errorMessage = "Cant be your own Manager";
        }
    } else if (model == "Prereqs") {
        if (data['PrereqID'] == data['MainCourseID']) {
            sendData = false;
            errorMessage = "A Course cant be its own Prereq";
        }
    }
    //switch (model) {
    //    case "All":
    //        $
    //        data['email'] = model 
    //        break;
    //}
    if (sendData) {
        sendEditFormData(data);
    }

    $("input[type=text], textarea").val("");
    $('#editModal').modal("hide");
}

function getKeys(model,item) {
    let id;
    let id2;
    console.log(model)
    if (item.hasAttribute('elementid2')) {
        id = item.getAttribute('elementid')
        id2 = item.getAttribute('elementid2')
        return [id, id2]
    } else {
        id = item.getAttribute('elementid');
        return id
    }
    
           
   
}

function sendEditFormData(data) {
    //console.log(data)
    $.ajax({
        method: 'POST',
        contentType: 'application/json',
        url: "/admin/edit",
        dataType: 'json',
        data: JSON.stringify(data),
        success: function (response) {

            console.log(response)
            addRow(response.data)
        },
        error: function (err) { console.log(err) }
    })
}


function sendAddFormData(data) {
    console.log(data)
    $.ajax({
        method: 'POST',
        contentType: 'application/json',
        url: "/admin/manage",
        dataType: 'json',
        data: JSON.stringify(data),
        success: function (response) {

            console.log(response)
            //addRow(response.data)
        },
        error: function (err) { console.log(err) } 
    })
}

function selectAll() {
    var checkbox = $('table tbody input[type="checkbox"]');
    this.checked = !this.checked;
    console.log(checkbox)
    if (this.checked) {
        checkbox.each(function () {
            this.checked = true;
        });
    } else {
        checkbox.each(function () {
            this.checked = false;
        });
    }
}



function deleteForm(event) {
    event.preventDefault();
    checkedItems = $('table tbody input[type="checkbox"]:checked');
    console.log(checkedItems);
    var model = $('#modaldeleteItemTitle').html();
    if (itemToDelete == undefined) {
        
        var checkbox = checkedItems;
        if (checkbox.length > 0) {
            var rows = [];
            var data = []
            console.log(checkbox);
            checkbox.each(function () {
                if (this.checked) {

                    rows.push(this.parentNode.parentNode.rowIndex);
                    data.push({ "id": getKeys(model, this.parentNode.parentNode), "model": model });
                }
            })
            console.log(data, rows)
            deletePost(data, rows, deleteRowCallback);
        }
        
    } else {
        let rows = [itemToDelete.rowIndex];
        let data = [{ "id": getKeys(model, itemToDelete), "model": model }];

        console.log(data);
        deletePost(data, rows, deleteRowCallback);
    }
    itemToDelete = undefined;
    $('#deleteModal').modal('hide');
}



function deleteRowCallback(rows) {
    let offset = 0;
    let previousRow = null;
    for (let row of rows) {
        console.log(row);
        if (previousRow == null) {
            document.getElementById("table").deleteRow(row);
            previousRow = row;
        } else {
            if (previousRow > row) {
                document.getElementById("table").deleteRow(row);
            } else {
                document.getElementById("table").deleteRow(row-1);
            }
        }
        
    }
    
}

var itemToDelete = undefined;

function deleteRow(r) {
    itemToDelete = r.parentNode.parentNode.parentNode;

    console.log(itemToDelete)
    $('#deleteModal').modal('show');
}

function editRow(r) {
    let rowNode = r.parentNode.parentNode.parentNode;
    let id;
    if (rowNode.hasAttribute("elementID2")) {
        id = (rowNode.getAttribute("elementID"), rowNode.getAttribute("elementID2"));
    } else {
        id = rowNode.getAttribute("elementID")
    }
    
    //console.log(rowNode.getAttribute("elementID"));
    for (var item of currentTableEntries) {
        if (id == getEntryID(item)) {
            //console.log(item);
            addIDToForm(item);
            //$("#editModalContentForm").attr("elementID", id);
            populate("#editModalContentForm", item);
        }
    }
    $('#editModal').modal('show');
}

function addIDToForm(item) {
    switch (item.model) {
        case "All":
            id = item.PersonID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Prereqs":
            id = item.MainCourseID;
            $("#editModalContentForm").attr("elementID", id);
            id2 = item.PrereqID;
            $("#editModalContentForm").attr("elementID2", id2);
            break;
        default:
            break;
    }
}



function getEntryID(entry) {
    var id;
    switch (entry.model) {
        case "All":
            id = entry.PersonID;
            break;
        case "Prereqs":
            id = (entry.MainCourseID, entry.PrereqID)
        default:
            break;
    }
    return id;
}

//found on https://stackoverflow.com/questions/7298364/using-jquery-and-json-to-populate-forms
function populate(frm, data) {
    $.each(data, function (key, value) {
        var ctrl = $('[name=' + key + ']', frm);
        switch (ctrl.prop("type")) {
            case "checkbox":
                ctrl.each(function () {
                    if ($(this).attr('name') == key) $(this).attr("checked", convertToBoolean(value));
                });
                break;
            default:
                ctrl.val(value);
        }
    });
}


function cancelDelete() {
    itemToDelete = undefined;
}

function deletePost(data, rows, callback) {
    $.ajax({
        method: 'POST',
        contentType: 'application/json',
        url: "/admin/delete",
        dataType: 'json',
        data: JSON.stringify(data),
        success: function (response) {
            console.log(response);
            callback(rows);
        }
    })
}


function addRow(rowData) {
    console.log(rowData);
    var row = document.createElement('tr');

    switch (rowData['model']) {
        case "All":
            row.setAttribute("elementid", rowData['PersonID']);
            break;
        default:
            break;
    }
        
    //html += '<tr elementid=' + array[i].PersonID + '><td>' +
    //    '<input type="checkbox" id="checkbox' + i + '" name="options[]" value="1">' +
    //    '<label for="checkbox1"></label>' + '</td><td>' + array[i].FName + ' ' + array[i].LName + '</td><td>' +
    //    array[i].Email + '</td><td>' + array[i].UserType + '</td><td>' + array[i].PhoneNum + '</td><td>' +
    //    convertToBoolean(array[i].Manager) + '</td><td>'
    //    + '<a href="#editModal" class="edit" data-toggle="modal"><i class="material-icons"' +
    //    'data-toggle="tooltip" title="Edit">&#xE254;</i></a>' +
    //    '<a class="delete" ><i class="material-icons"' +
    //    'data-toggle="tooltip" title="Delete" onclick="deleteRow(this);">&#xE872;</i></a>' + '</td></tr>';

}