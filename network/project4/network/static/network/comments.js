document.addEventListener('DOMContentLoaded', function() {

  var comment = document.querySelector('#comment-input')
  document.querySelector('#commentsubmit').addEventListener('click', () => {
    fetch('/comments', {
      method: 'POST',
      body: JSON.stringify({
          comment: comment.value,
      })
    })
    
    })

})