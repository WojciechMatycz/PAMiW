var firstname = document.getElementsByName('firstname')[0]
console.log(firstname)

function is_alpha(str){
 regexp = /^[A-Za-z]+$/;

        if (regexp.test(str))
          {
            return true;
          }
        else
          {
            return false;
          }
}

firstname.onblur = function(ev){
	if(!is_alpha(firstname))
		console.log("To nie jest za łądne imie")
}