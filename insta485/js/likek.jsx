import React, {Component} from "react";

class Demo2 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            qn: props.qn,
            qi: props.qi,
        };
        this.onValueChange = this.onValueChange.bind(this);
        this.formSubmit = this.formSubmit.bind(this);
    }

    onValueChange(event) {
        this.setState({
            selectedOption: event.target.value
        });
    }

    formSubmit(event) {
        event.preventDefault();
        console.log(this.state);
        let url = "/record/"
        fetch(
            url,
            {
                credentials: 'same-origin',
                method: 'POST',
                headers: {Content_Type: 'application/json'},
                body: JSON.stringify({qn: this.state.qn, qi: this.state.qi, choice:this.state.selectedOption}),
            },
        )
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
            })
            .catch((error) => console.log(error));
    }

    render() {
        return (
            <form onSubmit={this.formSubmit}>
                <input
                    type="radio"
                    value="1"
                    checked={this.state.selectedOption === "1"}
                    onChange={this.onValueChange}
                />
                是/Yes
                <input
                    type="radio"
                    value="0"
                    checked={this.state.selectedOption === "0"}
                    onChange={this.onValueChange}
                />
                否/No
                {/*<div>*/}
                {/*  Selected option is : {this.state.selectedOption}*/}
                {/*</div>*/}
                <button className="btn btn-default" type="submit">
                    Submit
                </button>
            </form>
        )
            ;
    }
}

export default Demo2;