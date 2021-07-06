/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:8080', // the running FLASK api server url
  auth0: {
    url: 'tnmayer.eu', // the auth0 domain prefix
    audience: 'fsnd_coffee_shop', // the audience set for the auth0 app
    clientId: 'OTyexCMUnINd1UgH3oAmZR7EhpM4R9uU', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
