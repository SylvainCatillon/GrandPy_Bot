$(function() {
	$("#user_form").on("submit", function(event) {
		message = $("#user_message").val();
		$("#dialog_box").append("<p>" + message + "</p>");
		event.preventDefault();
		event.stopPropagation();
		$('#user_form').trigger("reset");
	})
})