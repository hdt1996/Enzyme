class BrowserUtils
{
  constructor()
  {
    this.checkattributes = ({element, attrib}) =>
    {
      this.element_defaults = {'css':{}, 'style':{}}
      if(attrib === 'text')
      {
        {
          if(element.innerText !== undefined)
          {
            return element.innerText
          }
          else
          {
            return ''
          }
        }
      }
      else if (attrib === 'innerHTML' && element.innerHTML !== undefined)
      {
        return element.innerHTML
      }
      else if (attrib === 'style')
      {
        return this.buildDictKV({arr:element.getAttribute(attrib).split(";"),delim:':'})
      }
      else
      {
        return element.getAttribute(attrib) 
      }

    };
    this.buildAttribDict = ({element}) =>
    {
      let result_dict = {}
      let prop_names = element.getAttributeNames().toString().split(",");
      for(let att = 0; att < prop_names.length; att++)
      {
        if(prop_names[att] === '' || prop_names[att] === null)
        {
          continue
        };
        result_dict[prop_names[att]] = this.checkattributes({element:element,attrib:prop_names[att]})
      }
      return result_dict
    }
    this.buildDictBool = ({arr}) => 
    {
      let bool_dict = {}
      for(let i = 0; i < arr.length; i++)
      {
        if(arr[i] === "")
        {
          continue
        }
        bool_dict[arr[i]] = true
      }
      return bool_dict
    }

    this.buildDictKV = ({arr, delim = null}) =>
    {
      let key, value
      let kv_dict = {}
      for(let i = 0; i < arr.length; i++)
      {
        if(delim !== null)
        {
          let split_data = arr[i].split(delim)
          key = split_data[0]
          value = split_data[1]
        }
        
        if(key && value)
        {
          kv_dict[key] = value
        }
        else
        {
          kv_dict[arr[i]] = true
        }
      }
      return kv_dict
    }
    this.pullKeyfromDict = ({dict, key}) =>
    {
      if(dict[key] !== undefined)
      {
        return dict[key]
      }
      if(key in this.element_defaults)
      {
        return this.element_defaults[key]
      }
      return ''
    }
  }

}

export class Selenium extends BrowserUtils
{
  constructor({target = '',props = ['text','aria-label'], action = 'match', xpath = null})
  {
    super();
    this.props = props;
    this.target = target;
    this.action = action;
    this.xpath = xpath;
    this.HTML_MAPPING = {}
    this.MATCH = [];
    this.EL_BY_XPATH= null

    this.processAction = ({selector}) =>
    {
      if(this.action === 'match')
      {
        this.HTML_MAPPING = this.buildElementGrid({element: document.querySelector(selector)})
        console.log(this.MATCH)
        return this.MATCH
      }
      if(this.action === 'grid')
      {
        this.HTML_MAPPING = this.buildElementGrid({element: document.querySelector(selector)})
        console.log(this.HTML_MAPPING)
        return this.HTML_MAPPING
      }
      if(this.action === 'xpath')
      {
        this.HTML_MAPPING = this.buildElementGrid({element: document.querySelector(selector)});
        return this.EL_BY_XPATH
      }
      return 'Requested Process does not exist. Please choose Match or Grid.'

    }

    this.buildElementGrid = ({element, grid_id = [0], c_id = null, n = 0}) =>
    {
      let match_vals = {};
      match_vals['css'] = this.buildDictBool({arr:element.className.toString().split(/\s+/)})
      match_vals['text'] = this.checkattributes({element: element,attrib:'text'})
      match_vals['properties'] = this.buildAttribDict({element:element})
      match_vals['scripts'] = this.pullKeyfromDict({dict: match_vals['properties'], key:'onclick'})
      match_vals['style'] = this.pullKeyfromDict({dict: match_vals['properties'],key:'style'})
      match_vals['type'] = 'element';
      match_vals['api_type'] = '';

      grid_id  =[...grid_id];
      if(c_id !== null){grid_id.push(c_id)};
      match_vals['TYG'] = grid_id;
      if(this.target !== null && this.props.length > 0 && this.action === 'match')
      {
        for(let prop = 0; prop < this.props.length; prop++)
        {
          if (this.target === this.checkattributes({element: element, attrib: this.props[prop]}))
          {
            this.MATCH.push({"element":element,"xpath":grid_id})
          }
        }
      }
      let id_index
      if(this.action === 'xpath' && n + 1< this.xpath.length)
      {
        id_index = this.xpath[n + 1] 
      }
      n = n + 1
      
      if(JSON.stringify(grid_id) === JSON.stringify(this.xpath) && this.action === 'xpath')
      {
        this.EL_BY_XPATH = element
      }
      let children = element.children;
      for(let i = 0; i < children.length; i++)
      {
        if(this.action === 'xpath')
        {
          if (id_index !== i){continue}
        }
        match_vals[i] = this.buildElementGrid({element:children[i],grid_id:grid_id,c_id:i, n: n})
      }
      return match_vals
    }
  }
};
