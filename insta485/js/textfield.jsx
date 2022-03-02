import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';

class TextField extends React.Component {
  constructor(props) {
    super(props);
    // this.state.url = props.url
    this.state = {
      url: props.url, text: '', update: props.addFunction, pid: props.pid,
    };
    // console.log(this.state)
    // this.state = {textEntry: '', name: null};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  // function called when user types in text field
  handleChange(event) {
    this.setState({ text: event.target.value });
    console.log(JSON.stringify({ text: this.state.text }));
  }

  // function called when user submits
  handleSubmit(event) {
    event.preventDefault();
    fetch(
      this.state.url,
      {
        credentials: 'same-origin',
        method: 'POST',
        headers: { Content_Type: 'application/json' },
        body: JSON.stringify({ text: this.state.text }),
      },
    )
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // console.log(data)
        // console.log(this.state)
        this.props.addFunction(data, this.state.pid);
      })
      .catch((error) => console.log(error));
    this.setState({
      text: '',
    });
    // prevents website from refreshing
  }

  // return Jsx
  render() {
    return (
      <div>
        <form className="comment-form" onSubmit={this.handleSubmit}>
          <label>
            <input className="ui input" type="text" value={this.state.text} onChange={this.handleChange} />
          </label>
          {/* <input type="submit" value="Submit" /> */}
        </form>
        {/* {this.state.name !== null ? (<h4>Hello {this.state.name} </h4>) : (null)} */}
      </div>
    );
  }
}

export default TextField;
