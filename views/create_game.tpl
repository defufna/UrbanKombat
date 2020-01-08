% rebase('base.tpl', title='Create game')
<div class="wrap">
    <div class="logo">
        <img src="/static/logo.png">
    </div>
    <div class="gp flav">
        <p>Urban Kombat is <a href="http://www.urbandead.com">Urban Dead</a> clone, focused on real time combat. You can use it for a quick UD showdown.</p>
        <p>The game is open source and source can be found on <a href="https://github.com/defufna/UrbanKombat">github</a></p>
    </div>
    <div class="gp flav">
        <strong>Create Game</strong>
        <form action="/create" method="POST">
            <fieldset>
                <legend>Game options</legend>
                <label>Game name (optional)</label>
                <input type="text" name="game_name">
            </fieldset>

            %include("create_char.tpl")

            <button class="marg m" type="submit">Create Game</button>
        </form>
    </div>
</div>