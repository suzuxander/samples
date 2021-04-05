export const handler = async (event: any, context: any, callback: any): Promise<any> => {
  callback(null, {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: 'OK' })
  });
};