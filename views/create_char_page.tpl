% rebase('base.tpl', title='Create character')
<div class="gp">    
    <form action="/{{format(game.id, "X")}}/create_char" method="POST">
        %include('create_char.tpl', pick_team=True)
        <button class="m marg" type="submit">Create</button>
    </form>
    <p>
        Current Teams:
        <%
        for team in game.teams:
            include("team_invite.tpl", team=team)
        end
        %>
    </p>    
</div>