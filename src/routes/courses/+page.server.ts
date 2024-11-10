import fs from 'fs/promises';
import path from 'path';
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions: Actions = {
	avatar: async ({ request, route, url }) => {
		try {
			const data = Object.fromEntries(await request.formData());
			console.log(process.cwd());
			const filePath = path.join(
				process.cwd(),
				'static',
				'avatars',
				`${crypto.randomUUID()}.${(data.avatar as Blob).type.split('/')[1]}`
			);
			//@ts-ignore
			await fs.writeFile(filePath, Buffer.from(await (data.avatar as Blob).arrayBuffer()));
			// let b = await Buffer.from(await (data.avatar as Blob).arrayBuffer());

			//
			// fetch('http://httpbin.org/post', {
			//     method: 'POST',
			//     body: b // Here, stringContent or bufferContent would also work
			// })
			//     .then(function(res) {
			//         return res.json();
			//     }).then(function(json) {
			//     console.log(json);
			// });

			// TODO: store the file path in database for further references.
			throw redirect(303, url.pathname);
		} catch (err) {
			console.log(err);
			// return  fail(500, { err: err })
		}
	}
};
