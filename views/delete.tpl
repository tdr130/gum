<div>
     <style scoped>
        .button-warning {
            float:right;
            background: rgb(202, 60, 60);
        }
     </style>
    <form action='/home/delete/{{title}}/{{id}}' method='POST'>
	    <input type='hidden' name='token' value='{{token}}'>
	    <input class='button-warning pure-button' type='submit' value='Delete'>
    </form>
</div>
