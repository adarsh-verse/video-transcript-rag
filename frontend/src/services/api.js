import axios from "axios"

const BASE_URL = "http://127.0.0.1:8000";

export const ProcessInput = async (file, url) =>{
    try{
        console.log("ProcessInput invoked...")
        let response;
        if (file){
            const formData = new FormData()
            formData.append("file", file)

            response = await axios.post(`${BASE_URL}/process`,formData)
            console.log(response)
        }

        else if (url){
            response = await axios.post(`${BASE_URL}/process`,null, {
                params:{
                    input_source: url,
                },
            }
        );
        }
        return response.data

    }
    catch (error){
        console.error(error)

    }
}

export const askQuestion = async (question) =>{
    try{
        const response = await axios.post(`${BASE_URL}/ask`,null,{
            params: {
                query: question,
            },
        });
        return response.data
    }
    catch (error){
        console.error(error);
        throw error;
    }  
}