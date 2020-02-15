$(function() {

	// Create a loading animation
	var loading =
		$('<div class="d-flex justify-content-center">\
			<div class="spinner-border text-info" role="status">\
			<span class="sr-only">Loading...</span></div></div>');

	var dialog_box = $("#dialog_box");

	async function showAnswer() {
		if (this.readyState == XMLHttpRequest.DONE) {
			loading.remove();
			if (this.status == 200) {
				var result = JSON.parse(this.responseText);
				if (result.status == "OK") {
					// Display the address
					$("<p></p>", {
						"class": "alert alert-success mx-3 rounded shadow-lg",
						text: result.address
					}).appendTo(dialog_box);

					// Display the map
					$("<iframe></iframe>", {
						"class": "mx-auto my-3 d-block",
						id: "map", frameborder: 0,
						style: "border: 0; width: 95%; height: 45%;",
						allowfullscreen: 1, src: result.map_url,
						text: "carte du lieu"
					}).appendTo(dialog_box);

					dialog_box.scrollTop(dialog_box[0].scrollHeight);

					// Await 3 sec before displaying the story
					await new Promise(r => setTimeout(r, 3000));
					$("<p></p>", {
						"class": "alert alert-success mx-3 rounded shadow-lg",
						text: result.story
					}).append($("<a></a>", {
						href: result.story_url,
						text: result.story_link_text
					})).appendTo(dialog_box);

				} else if (result.status == "ADDRESS_NOT_FOUND") {
					$("<p></p>", {
						"class": "alert alert-warning mx-3 rounded shadow-lg",
						text: result.message
					}).appendTo(dialog_box);
				} else {
					$("<p></p>", {
						"class": "alert alert-danger mx-3 rounded shadow-lg",
						text: result.message
					}).appendTo(dialog_box);
				} 
			}
		} else {
			dialog_box.append(loading);
		}
		dialog_box.scrollTop(dialog_box[0].scrollHeight);
	}

	function askQuestion(event) {
		var user_message = $("#user_message").val();
		event.preventDefault();
		event.stopPropagation();
		if (user_message) {
			// Display the question of the user
			$("<p></p>", {
				"class": "alert alert-info mx-3 rounded shadow-lg",
				text: user_message
			}).appendTo(dialog_box);

			// Send the question to the back-end
			var request = new XMLHttpRequest();
			request.onreadystatechange = showAnswer;
			var url =
				window.location.origin +
				"/get_answer?user_message=" +
				user_message;

			request.open("GET", url);
			request.send();
			$('#user_form').trigger("reset");
		}
	}

	$("#user_form").on("submit", askQuestion);
});