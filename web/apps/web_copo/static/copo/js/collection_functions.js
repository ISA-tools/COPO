function do_add_study_type() {
    var clonableTarget = $("#study_types_lists_div").children(":last").clone();

    //update id of cloned div
    var targetId = clonableTarget.attr("id");
    var splitIndex = targetId.lastIndexOf("_");
    var literalPart = targetId.substr(0, splitIndex + 1);
    var indexPart = targetId.substr(splitIndex + 1);

    clonableTarget.attr("id", literalPart + (parseInt(indexPart) + 1));


    // update the id, name of the study type select element
    var targetChild = clonableTarget.children(":nth-child(1)").children(":first");
    update_id_name_indx(targetChild);

    // update id, name of the cloned study type id text field
    targetChild = clonableTarget.children(":nth-child(2)").children(":first");
    targetChild.val("");
    update_id_name_indx(targetChild);

    // update id of anchor element
    targetChild = clonableTarget.children(":nth-child(3)").children(":first");
    update_id_name_indx(targetChild);

    //show the delete button for the cloned node
    clonableTarget.children(":nth-child(3)").children(":first").show();
    $("#study_types_lists_div").append(clonableTarget);
}

function update_id_name_indx(targetChild) {
    var targetId = targetChild.attr("id");
    var splitIndex = targetId.lastIndexOf("_");
    var literalPart = targetId.substr(0, splitIndex + 1);
    var indexPart = targetId.substr(splitIndex + 1);
    targetChild.attr("id", literalPart + (parseInt(indexPart) + 1));
    targetChild.attr("name", literalPart + (parseInt(indexPart) + 1));
}

function update_id_name_byref(targetChild, ref) {
    var targetId = targetChild.attr("id");
    var splitIndex = targetId.lastIndexOf("_");
    var literalPart = targetId.substr(0, splitIndex + 1);
    targetChild.attr("id", literalPart + ref);
}

function do_remove_study_type(event) {
    var targetId = $($(event.target)).parent().attr("id");
    var splitIndex = targetId.lastIndexOf("_");
    var indexPart = targetId.substr(splitIndex + 1);

    //remove the parent
    $("#study_type_select_divs_" + indexPart).remove();
}

function toggle_collection_type(collection_type) {
    if (collection_type.toLocaleLowerCase() == "ena submission") {
        $("#study_type_div").show();
    } else {
        $("#study_type_div").hide();
    }
}


