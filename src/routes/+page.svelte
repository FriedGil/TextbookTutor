<script>
    import Login from "$lib/Components/Login.svelte";
    import { page } from "$app/stores";
    import {goto} from "$app/navigation";
    $: loggedIn = $page.data.session != null;
    console.log($page.data.session);
</script>

<div class="content-center">

    {#if !loggedIn}
        {goto('/auth/signin', { replaceState: true })}

    {:else }
        <div
                class="hero min-h-screen"
                style="background-image: url(https://img.daisyui.com/images/stock/photo-1507358522600-9f71e620c44e.webp);">
            <div class="hero-overlay bg-opacity-60"></div>
            <div class="hero-content text-neutral-content text-center">
                <div class="max-w-md">
                    <h1 class="mb-5 text-5xl font-bold">Welcome Back</h1>
                    <p class="mb-5">
                        Jump into a variety of courses.
                    </p>
                    <a href="/courses">
                        <button class="btn btn-primary">Go to Courses</button>
                    </a>
                </div>
            </div>
        </div>
    {/if}
</div>