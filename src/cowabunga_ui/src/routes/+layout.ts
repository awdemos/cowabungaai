import type { LayoutLoad } from './$types';

export const load: LayoutLoad = async ({ data }) => {
  return {
    session: data.session,
    user: data.user,
    isUsingOpenAI: data.isUsingOpenAI
  };
};
