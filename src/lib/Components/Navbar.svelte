<script>

    let loggedIn = true;
    import { SignOut } from "@auth/sveltekit/components";
    import '../../app.css';


    function delay (URL) {
        setTimeout( function() { window.location = URL }, 500 );
    }

</script>

<div class="navbar bg-base-100">
    <div class="flex-1">
        <a class="btn btn-ghost text-xl" href="/">📚 Textbook Tutor</a>
    </div>
    <div class="flex-none">
        <ul class="menu menu-horizontal px-1">
            {#if loggedIn}
                <li>
                    <a href="#modal">
                        🔥&nbsp 1
                    </a>
                </li>
                <li><a href="/courses">Courses</a></li>
                <li>
                    <details>
                            <summary>Account</summary>
                            <ul class="bg-base-100 rounded-t-none p-2">
                                <li><a>Settings</a></li>
                                <li>
                                    <a on:click={()=>{delay('/auth/signin')}}>
                                        <SignOut>
                                            <span slot="submitButton">Log Out</span>
                                        </SignOut>
                                    </a>
                                </li>
                            </ul>
                    </details>
                </li>
            {:else}
                <li><a>About</a></li>
                <li><a>Pricing</a></li>
            {/if}
        </ul>
    </div>
</div>

<div class="modal" role="dialog" id="modal">
    <div class="modal-box">
        <h3 class="text-lg font-bold">You Have a One Day Streak.</h3>
        <p class="py-4">Keep it going!</p>
        <div class="modal-action">
            <a href="#" class="btn">Exit</a>
        </div>
    </div>
</div>
