var csrftoken = "";

/** closeEditPost
	Close all editable posts: Change textarea for div and hide save button
 */
function closeEditPost () {
	edtPosts = document.querySelectorAll(".spanEdit");
	edtPosts.forEach( item => { 
		let id = item.getAttribute('data-id');
		let textarea = document.querySelector(`#txt${id} > textarea[name="content"]`);
		if (textarea) {
			document.querySelector(`#txt${id}`).innerHTML = `${textarea.value.trim()}`;
			// Hide the save button
			document.querySelector(`#btn${id}`).style.display = "none";
		}
	});
} // closeEditPost

/** savePost 
	fetch a requirement to a view to save the post
 */
function savePost (object) {
	// Get relevant info from Span tag
	let id = object.getAttribute('data-id');
	let content = document.querySelector(`#txt${id} > textarea[name="content"]`).value;

	fetch('updatePost', {
		method: 'POST',
		headers: { 
			"X-CSRFToken": csrftoken, // Indispensable!!!!!
			"Accept": "application/json",
        	"Content-Type": "application/json; charset=utf-8",
			'X-Requested-With': 'XMLHttpRequest'
		},
		body: JSON.stringify({
			id: id,
			contents: content
		})
	})
	.then(response => {
		return response.json()
	})
	.then(resultJson => {
	    // alert (result.message)
	    console.log(resultJson);

		// Close all editable posts
		closeEditPost ();
	})
	.catch(function(error) {
    	console.log("Error", error);
	});
} // savePost

/** editPost
	Provide a textarea for editing a post content  
 */
function editPost (object) {
	// Close all editable posts
	closeEditPost ()
	
	// Get relevant info from Span tag
	let id = object.getAttribute('data-id');
	let contentDiv = document.querySelector(`#txt${id}`);
	let content = contentDiv.innerHTML;

	// Make the current post ready to edit
	contentDiv.innerHTML = `<textarea name="content">${content.trim()}</textarea>`;
	document.querySelector(`#txt${id} > textarea[name="content"]`).focus();

	// Unhide the save button
	document.querySelector(`#btn${id}`).style.display = "block";
} // editPost

function updateTotalLikes (idPost, totallikes) {
	let field = document.querySelector(`#likes${idPost}`).innerHTML = `(${totallikes})`;
} // updateTotalLikes

function likePost (object) {
	// Get relevant data
	let id = object.getAttribute('data-id');
	let iclass = object.getAttribute('class');
	var like = false; 

	if (iclass.search("enabled") != -1) {
		iclass = iclass.replace("enabled","disabled");
		like = false;
	}
	else if  (iclass.search("disabled") != -1) {
		iclass = iclass.replace("disabled","enabled");
		like = true;
	}
	object.setAttribute("class", iclass);

	// Update likes
	fetch('likePost', {
		method: 'POST',
		headers: { 
			"X-CSRFToken": csrftoken, // Indispensable!!!!!
			"Accept": "application/json",
        	"Content-Type": "application/json; charset=utf-8",
			'X-Requested-With': 'XMLHttpRequest'
		},
		body: JSON.stringify({
			id: id,
			like: like
		})
	})
	.then(response => {
		return response.json()
	})
	.then(resultJson => {
	    updateTotalLikes (id, parseInt(resultJson.totallikes));
	    console.log(resultJson.message);
	})
	.catch(function(error) {
    	console.log("Error", error);
	});	
/*
<i class="fas fa-thumbs-up likeIcon disabled" data-id="{{p.pk}}"></i>
<span id="likes{{p.pk}}" class="totalLikes">({{ p.totallikes }})</span>	
*/
} // likePost


/** When load page */
document.addEventListener('DOMContentLoaded', load);
/** Load
 * - Set "onclick" event handlers
 */
function load () {

	/** Click event handler for "Edit" post
     */
	document.querySelectorAll('.spanEdit').forEach ( item => {
		// Onclick on edit span
		item.addEventListener('click', event => { editPost(item) });

		// Onclick on save button -- All relevant info is in the Span element
		let id = item.getAttribute('data-id');
		let elem = document.querySelector(`#btn${id}`);
		elem.addEventListener('click', event => { savePost(item) });		
	}); // End .spanEdit'.onclick

	/** Click event handler for "Like" post
	 */
	document.querySelectorAll('.likeIcon').forEach ( item => {
		// Onclick on like icon span
		item.addEventListener('click', event => { likePost(item) });
	}); // End .likeIcon'.onclick

	csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
} // End load

