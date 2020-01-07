% rebase('base.tpl', title='Create character')
<form action="create_char" method="POST">
    %include('create_char.tpl', team=team)
    <button type="submit">Create</button>
</form>
