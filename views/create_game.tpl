% rebase('base.tpl', title='Create game')
<form action="/create" method="POST">
    <fieldset>
        <legend>Game options</legend>
        <label>Game name (optional)</label>
        <input type="text" name="game_name">
    </fieldset>
    
    %include("create_char.tpl")
    
    <button type="submit">Create</button>
</form>
