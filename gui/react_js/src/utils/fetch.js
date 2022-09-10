  export class Fetch
  {
    constructor(api_url)
    {
        this.options = {}
        this.url = api_url
        this.makeOption = ({crud = 'GET',add_headers = {},body = null})=>
        {
            let options = {}
            options["method"] = crud
            options['headers'] = {'Content-Type':'application/json'}
            if(Object.keys(add_headers).length > 0)
            {
                for(let key in add_headers)
                {
                    options['headers'][key] = JSON.stringify(add_headers[key])
                }
            }
            if(crud !== 'GET')
            {
                options['body'] = JSON.stringify(body)
            }
            this.options = options
            console.log(this.options)
        }
        this.fetch = async () =>
        {
            let response = await fetch(this.url,this.options)
            let data = await response.json()
            this.options = {}
            return data
        }
    }

    
  }
  
  
  