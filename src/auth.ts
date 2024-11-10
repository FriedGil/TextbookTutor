import { SvelteKitAuth } from '@auth/sveltekit';
import { MongoDBAdapter } from '@auth/mongodb-adapter';
import client from './lib/db';
import Google from '@auth/sveltekit/providers/google';
import { AUTH_SECRET } from '$env/static/private';

//@ts-ignore

export const { handle, signIn, signOut } = SvelteKitAuth(async (event) => {
	const authOptions = {
		adapter: MongoDBAdapter(client),
		providers: [Google],
		secret: AUTH_SECRET,
		trustHost: true
	};
	return authOptions;
});
