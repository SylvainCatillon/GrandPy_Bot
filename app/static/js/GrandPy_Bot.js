$(function() {
	var loading = $('<div class="d-flex justify-content-center"><div class="spinner-border text-info" role="status"><span class="sr-only">Loading...</span></div></div>')

	$("#user_form").on("submit", function(event) {
		var user_message = $("#user_message").val();
		event.preventDefault();
		event.stopPropagation();
		if (user_message) {
			var dialog_box = $("#dialog_box");
			$("<p></p>", {"class": "alert alert-info mx-3 rounded shadow-lg", text: user_message}).appendTo(dialog_box);
			var request = new XMLHttpRequest();
			request.onreadystatechange = function() {
				if (this.readyState == XMLHttpRequest.DONE) {
					loading.remove()
					if (this.status == 200) {
						var result = JSON.parse(this.responseText);
						if (result.status == "OK") {
							$("<p></p>", {"class": "alert alert-success mx-3 rounded shadow-lg", text: result.address}).appendTo(dialog_box)
							var map = $("<img>", {"class": "d-block my-3 mx-auto", id: "map", src: result.static_map_url, alt: "carte du lieu"})
							map.on("load", function() {
								dialog_box.scrollTop(dialog_box[0].scrollHeight);
								})
							map.appendTo(dialog_box)
							//attention texte dans js, à eviter!!
							$("<p></p>", {"class": "alert alert-success mx-3 rounded shadow-lg", text: result.story}).append($("<a></a>", {href: result.story_url, text: result.story_link_text})).appendTo(dialog_box)
						} else if (result.status == "address_not_found") {
							$("<p></p>", {"class": "alert alert-warning mx-3 rounded shadow-lg", text: result.message}).appendTo(dialog_box)
						}
					} else {
						// attention, message dans js, à eviter
						$("<p></p>", {"class": "alert alert-danger mx-3 rounded shadow-lg", text: "Houla, je crois que ma connexion ne marche pas bien.. Ca doit etre l'age!!"}).appendTo(dialog_box)
					}
				} else {
					dialog_box.append(loading);
				} dialog_box.scrollTop(dialog_box[0].scrollHeight);
			}
			var url = window.location.origin + "/get_response?user_message=" + user_message;
			request.open("GET", url);
			request.send();
			$('#user_form').trigger("reset");
		}
	})
})