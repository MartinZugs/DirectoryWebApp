
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
            opt.text = option.CourseName //might be switched to CourseName //todo
            break;
        case "PrereqID":
            opt.value = option.CourseID;
            opt.text = option.CourseName //might be switched to CourseName //todo
            break;
        case "CourseID":
            opt.value = option.CourseID;
            opt.text = option.CourseName //might be switched to CourseName //todo
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
            console.log(currentTableEntries);
            for (let row of response) {
                addRow(row);
            }
            //fillTable(response);
        }
    })
}


//function fillTable(array) {
//    if (array != null) {
//        $("#amountOfEntries").text(array.length);
//        var html = '';
//        for (var i = 0; i < array.length; i++) {
//            html += '<tr elementid="' + array[i].MainCourseID + '" elementid2=' + array[i].PrereqID + '><td>' +
//                '<input type="checkbox" id="checkbox'+i+'" name="options[]" value="1">' +
//                '<label for="checkbox1"></label>' + '</td><td>' + array[i].FName + ' ' + array[i].LName + '</td><td>' +
//                array[i].Email + '</td><td>' + array[i].UserType + '</td><td>' + array[i].PhoneNum + '</td><td>' +
//                convertToBoolean(array[i].Manager) + '</td><td>'
//                + '<a href="#editModal" class="edit" data-toggle="modal"><i class="material-icons"' +
//                'data-toggle="tooltip" title="Edit" onclick="editRow(this);">&#xE254;</i></a>' +
//                '<a class="delete" ><i class="material-icons"' +
//                'data-toggle="tooltip" title="Delete" onclick="deleteRow(this);">&#xE872;</i></a>' + '</td></tr>';

//        }
//        $('#table tbody').append(html);
//    }
    
//}

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
    console.log(data)
    $.ajax({
        method: 'POST',
        contentType: 'application/json',
        url: "/admin/edit",
        dataType: 'json',
        data: JSON.stringify(data),
        success: function (response) {

            console.log(response)
            if (Array.isArray(response.data)) {
                for (let item of response.data) {
                    updateRow(item)
                    
                }
            } else {
                updateRow(response.data)
                
            }
            
        },
        error: function (err) { console.log(err) }
    })
}

function updateRow(item) {
    console.log(item)
    
        $('tr').each(function () {
            if (this.hasAttribute("elementID2")) {
                if ((this.getAttribute("elementID"), this.getAttribute("elementID")) == getEntryID(item)) {
                    this.remove();
                    addRow(item);
                }
            }
            else if (this.getAttribute("elementID") == getEntryID(item)) {
                this.remove();
                addRow(item);
            }
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
            console.log(item);
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
        case "Enrolled_In":
            id = item.MainCourseID;
            $("#editModalContentForm").attr("elementID", id);
            id2 = item.PrereqID;
            $("#editModalContentForm").attr("elementID2", id2);
            break;
        case "Registered_For":
            id = item.MainCourseID;
            $("#editModalContentForm").attr("elementID", id);
            id2 = item.PrereqID;
            $("#editModalContentForm").attr("elementID2", id2);
            break;
        case "Student":
            id = item.StudentID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Employee":
            id = item.EmployeeID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Campus":
            id = item.CampusID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Building":
            id = item.BuildingID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Department":
            id = item.DepartmentID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Office":
            id = item.OfficeID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Faculty":
            id = item.EmployeeID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Course":
            id = item.CourseID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Undergrad":
            id = item.StudentID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Graduate":
            id = item.StudentID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Teaching_Assistant":
            id = item.StudentID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Research_Assistant":
            id = item.StudentID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Alumni":
            id = item.StudentID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Retiree":
            id = item.EmployeeID;
            $("#editModalContentForm").attr("elementID", id);
            break;
        case "Staff":
            id = item.EmployeeID;
            $("#editModalContentForm").attr("elementID", id);
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
            break;
        case "Enrolled_In":
            id = (entry.StudentID, entry.CourseID)
            break;
        case "Registered_For":
            id = (entry.StudentID, entry.CourseID)
            break;
        case "Student":
            id = entry.StudentID;
            break;
        case "Employee":
            id = entry.EmployeeID;
            break;
        case "Campus":
            id = entry.CampusID;
            break;
        case "Building":
            id = entry.BuildingID;
            break;
        case "Department":
            id = entry.DepartmentID;
            break;
        case "Office":
            id = entry.OfficeID;
            break;
        case "Faculty":
            id = entry.EmployeeID;
            break;
        case "Course":
            id = entry.CourseID;
            break;
        case "Undergrad":
            id = entry.StudentID;
            break;
        case "Graduate":
            id = entry.StudentID;
            break;
        case "Teaching_Assistant":
            id = entry.StudentID;
            break;
        case "Research_Assistant":
            id = entry.StudentID;
            break;
        case "Alumni":
            id = entry.StudentID;
            break;
        case "Retiree":
            id = entry.EmployeeID;
            break;
        case "Staff":
            id = entry.EmployeeID;
            break;
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

var counter = 0;

function addRow(rowData) {
    //console.log(rowData);
    var row = document.createElement('tr');

    var checkboxtd = document.createElement('td');
    var checkbox = document.createElement("input");
    checkbox.type = 'checkbox';
    checkbox.id = "checkbox" + counter;
    checkbox.value = 1;
    checkboxtd.append(checkbox);
    row.append(checkboxtd);

    if (rowData['model'] == "All") {
        row.setAttribute("elementid", rowData['PersonID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(name);
        let email = document.createElement('td');
        email.innerHTML = rowData['Email'];
        row.append(email);
        let phoneNum = document.createElement('td');
        phoneNum.innerHTML = rowData['PhoneNum'];
        row.append(phoneNum);
        let userType = document.createElement('td');
        userType.innerHTML = rowData['UserType'];
        row.append(userType);
        
        let manager = document.createElement('td');
        manager.innerHTML = convertToBoolean(rowData['Manager']);
        row.append(manager);
    } else if (rowData['model'] == "Student") {
        row.setAttribute("elementid", rowData['StudentID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(name);
        let email = document.createElement('td');
        email.innerHTML = rowData['Email'];
        row.append(email);
        let phoneNum = document.createElement('td');
        phoneNum.innerHTML = rowData['PhoneNum'];
        row.append(phoneNum);
        let studentType = document.createElement('td');
        studentType.innerHTML = rowData['StudentType'];
        row.append(studentType);
        let enrollmentStatus = document.createElement('td');
        enrollmentStatus.innerHTML = rowData['EnrollmentStatus'];
        row.append(enrollmentStatus);
        let creditHoursTotal = document.createElement('td');
        creditHoursTotal.innerHTML = rowData['CreditHoursTotal'];
        row.append(creditHoursTotal);
    } else if (rowData['model'] == "Employee") {
        row.setAttribute("elementid", rowData['EmployeeID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(name);
        let email = document.createElement('td');
        email.innerHTML = rowData['Email'];
        row.append(email);
        let phoneNum = document.createElement('td');
        phoneNum.innerHTML = rowData['PhoneNum'];
        row.append(phoneNum);
        let employeeType = document.createElement('td');
        employeeType.innerHTML = rowData['EmployeeType'];
        row.append(employeeType);
        
        let managerID = document.createElement('td');
        if (rowData['ManagerID'] == null) {
            managerID.innerHTML = "None";
        } else {
            managerID.innerHTML = rowData['ManagerID'];
        }
        row.append(managerID);
    } else if (rowData['model'] == "Faculty") {
        row.setAttribute("elementid", rowData['EmployeeID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(name);
        let email = document.createElement('td');
        email.innerHTML = rowData['Email'];
        row.append(email);
        let phoneNum = document.createElement('td');
        phoneNum.innerHTML = rowData['PhoneNum'];
        row.append(phoneNum);
        let officeID = document.createElement('td');
        if (rowData['OfficeID'] == null) {
            officeID.innerHTML = "None";
        } else {
            officeID.innerHTML =  rowData['BuildingName']+' '+rowData['OfficeID'];
        }
        row.append(officeID);
        let departmentID = document.createElement('td');
        departmentID.innerHTML = rowData['DepartmentName'];
        row.append(departmentID);
    } else if (rowData['model'] == "Undergrad") {
        row.setAttribute("elementid", rowData['StudentID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(name);
        let email = document.createElement('td');
        email.innerHTML = rowData['Email'];
        row.append(email);
        let phoneNum = document.createElement('td');
        phoneNum.innerHTML = rowData['PhoneNum'];
        row.append(phoneNum);
        
        let enrollmentStatus = document.createElement('td');
        enrollmentStatus.innerHTML = rowData['EnrollmentStatus'];
        row.append(enrollmentStatus);
        let creditHoursTotal = document.createElement('td');
        creditHoursTotal.innerHTML = rowData['CreditHoursTotal'];
        row.append(creditHoursTotal);
    } else if (rowData['model'] == "Graduate") {
        row.setAttribute("elementid", rowData['StudentID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(name);
        let email = document.createElement('td');
        email.innerHTML = rowData['Email'];
        row.append(email);
        let phoneNum = document.createElement('td');
        phoneNum.innerHTML = rowData['PhoneNum'];
        row.append(phoneNum);

        let enrollmentStatus = document.createElement('td');
        enrollmentStatus.innerHTML = rowData['EnrollmentStatus'];
        row.append(enrollmentStatus);
        let uGCompDate = document.createElement('td');
        uGCompDate.innerHTML = rowData['UGCompDate'];
        row.append(uGCompDate);
        let graduateType = document.createElement('td');
        if (rowData['GraduateType'] == null) {
            graduateType.innerHTML = 'None';
        } else {
            graduateType.innerHTML = rowData['GraduateType'];
        }
        row.append(graduateType);
    } else if (rowData['model'] == "Enrolled_In") {
        row.setAttribute("elementid", rowData['StudentID']);
        row.setAttribute("elementid2", rowData['CourseID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(name);
        let email = document.createElement('td');
        email.innerHTML = rowData['Email'];
        row.append(email);
        let phoneNum = document.createElement('td');
        phoneNum.innerHTML = rowData['PhoneNum'];
        row.append(phoneNum);

        let courseDescription = document.createElement('td');
        courseDescription.innerHTML = rowData['CourseDescription'];
        row.append(courseDescription);
        let credits = document.createElement('td');
        credits.innerHTML = rowData['Credits'];
        row.append(credits);
        
    } else if (rowData['model'] == "Registered_For") {
        row.setAttribute("elementid", rowData['StudentID']);
        row.setAttribute("elementid2", rowData['CourseID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(name);
        let email = document.createElement('td');
        email.innerHTML = rowData['Email'];
        row.append(email);
        let phoneNum = document.createElement('td');
        phoneNum.innerHTML = rowData['PhoneNum'];
        row.append(phoneNum);

        let courseDescription = document.createElement('td');
        courseDescription.innerHTML = rowData['CourseDescription'];
        row.append(courseDescription);
        let credits = document.createElement('td');
        credits.innerHTML = rowData['Credits'];
        row.append(credits);

    } else if (rowData['model'] == "Teaching_Assistant") {
        row.setAttribute("elementid", rowData['StudentID']);
        row.setAttribute("elementid2", rowData['CourseID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(name);
        let email = document.createElement('td');
        email.innerHTML = rowData['Email'];
        row.append(email);
        let phoneNum = document.createElement('td');
        phoneNum.innerHTML = rowData['PhoneNum'];
        row.append(phoneNum);

        let courseDescription = document.createElement('td');
        courseDescription.innerHTML = rowData['CourseDescription'];
        row.append(courseDescription);
        let credits = document.createElement('td');
        credits.innerHTML = rowData['Credits'];
        row.append(credits);

    } else if (rowData['model'] == "Research_Assistant") {
        row.setAttribute("elementid", rowData['StudentID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(name);
        let email = document.createElement('td');
        email.innerHTML = rowData['Email'];
        row.append(email);
        let phoneNum = document.createElement('td');
        phoneNum.innerHTML = rowData['PhoneNum'];
        row.append(phoneNum);

        let researchFocus = document.createElement('td');
        researchFocus.innerHTML = rowData['ResearchFocus'];
        row.append(researchFocus);

    } else if (rowData['model'] == "Campus") {
        row.setAttribute("elementid", rowData['CampusID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['CampusName'];
        row.append(name);
    } else if (rowData['model'] == "Building") {
        row.setAttribute("elementid", rowData['BuildingID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['BuildingName'];
        row.append(name);
        let buildingAddress = document.createElement('td');
        buildingAddress.innerHTML = rowData['BuildingAddress'];
        row.append(buildingAddress);
        let campusName = document.createElement('td');
        campusName.innerHTML = rowData['CampusName'];
        row.append(campusName);
    } else if (rowData['model'] == "Department") {
        row.setAttribute("elementid", rowData['DepartmentID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['DepartmentName'];
        row.append(name);
        let buildingName = document.createElement('td');
        buildingName.innerHTML = rowData['BuildingName'];
        row.append(buildingName);
    } else if (rowData['model'] == "Office") {
        row.setAttribute("elementid", rowData['OfficeID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['OfficeID'];
        row.append(name);
        let buildingName = document.createElement('td');
        buildingName.innerHTML = rowData['BuildingName'];
        row.append(buildingName);
    } else if (rowData['model'] == "Course") {
        row.setAttribute("elementid", rowData['CourseID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['CourseName'];
        row.append(name);
        let courseDescription = document.createElement('td');
        courseDescription.innerHTML = rowData['CourseDescription'];
        row.append(courseDescription);
        let profID = document.createElement('td');
        profID.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(profID);

        let noOfSeats = document.createElement('td');
        noOfSeats.innerHTML = rowData['NoOfSeats'];
        row.append(noOfSeats);
        let credits = document.createElement('td');
        credits.innerHTML = rowData['Credits'];
        row.append(credits);
    } else if (rowData['model'] == "Prereqs") {
        row.setAttribute("elementid", rowData['MainCourseID']);
        row.setAttribute("elementid2", rowData['PrereqID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['CourseName'];
        row.append(name);
        let courseDescription = document.createElement('td');
        courseDescription.innerHTML = rowData['CourseDescription'];
        row.append(courseDescription);
        let profID = document.createElement('td');
        profID.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(profID);

        let preName = document.createElement('td');
        preName.innerHTML = rowData['preName'];
        row.append(preName);
        
    } else if (rowData['model'] == "Alumni") {
        row.setAttribute("elementid", rowData['StudentID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(name);
        let email = document.createElement('td');
        email.innerHTML = rowData['Email'];
        row.append(email);
        let phoneNum = document.createElement('td');
        phoneNum.innerHTML = rowData['PhoneNum'];
        row.append(phoneNum);
        let graduationDate = document.createElement('td');
        
        graduationDate.innerHTML = "None";
        graduationDate.innerHTML = rowData['GraduationDate'];
        row.append(graduationDate);
        let finalSemester = document.createElement('td');
        finalSemester.innerHTML = rowData['FinalSemester'];
        row.append(finalSemester);
    } else if (rowData['model'] == "Retiree") {
        row.setAttribute("elementid", rowData['EmployeeID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(name);
        let email = document.createElement('td');
        email.innerHTML = rowData['Email'];
        row.append(email);
        let phoneNum = document.createElement('td');
        phoneNum.innerHTML = rowData['PhoneNum'];
        row.append(phoneNum);
        let retirementDate = document.createElement('td');
        retirementDate.innerHTML = rowData['RetirementDate'];
        row.append(retirementDate);
        let retirementPackage = document.createElement('td');
        retirementPackage.innerHTML = rowData['RetirementPackage'];
        row.append(retirementPackage);
    } else if (rowData['model'] == "Staff") {
        row.setAttribute("elementid", rowData['EmployeeID']);
        let name = document.createElement('td');
        name.innerHTML = rowData['FName'] + " " + rowData['LName'];
        row.append(name);
        let email = document.createElement('td');
        email.innerHTML = rowData['Email'];
        row.append(email);
        let phoneNum = document.createElement('td');
        phoneNum.innerHTML = rowData['PhoneNum'];
        row.append(phoneNum);
        let officeID = document.createElement('td');
        if (rowData['OfficeID'] == null) {
            officeID.innerHTML = "None";
        } else {
            officeID.innerHTML = rowData['BuildingName'] + ' ' + rowData['OfficeID'];
        }
        row.append(officeID);
        let departmentID = document.createElement('td');
        departmentID.innerHTML = rowData['DepartmentName'];
        row.append(departmentID);
    }
         
    

    var actionsTd = document.createElement("td");
    
    actionsTd.id = "action" + counter;
    let html = jQuery.parseHTML('<a href="#editModal" class="edit" data-toggle="modal"><i class="material-icons"' +
        'data-toggle="tooltip" title="Edit" onclick="editRow(this);">&#xE254;</i></a>');
        
    let html2 =   jQuery.parseHTML('<a class="delete" ><i class="material-icons"' +
        'data-toggle="tooltip" title="Delete" onclick="deleteRow(this);">&#xE872;</i></a>');
    
    row.append(actionsTd);
    
    $('#table tbody').append(row);
    $('#action' + counter).append(html);
    $('#action' + counter).append(html2);
    counter += 1;
  

}