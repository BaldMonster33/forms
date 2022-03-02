import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import TextField from './textfield'
import Demo2 from './likek'
import Comment from './comment'
import InfiniteScroll from 'react-infinite-scroll-component';
// import { useHistory } from "react-router-dom";

// import '/insta485/static/css/style.css';

class Post extends React.Component {
    /* Display number of image and post owner of a all posts
     */

    constructor(props) {
        // Initialize mutable state
        super(props);
        // this.state = { imgUrl: '', owner: '' };
        this.state = {questions: [], startidx: 0}
        this.submitfunction = this.submitfunction.bind(this);
        // this.addComment = this.addComment.bind(this);
        // this.deleteComment = this.deleteComment.bind(this);
        // this.likefunction = this.likefunction.bind(this);
        // this.unlikefunction = this.unlikefunction.bind(this);
    }


    componentDidMount() {
        // This line automatically assigns this.props.url to the const variable url
        const {url} = this.props;
        // Call REST API to get the post's information
        fetch(url, {credentials: 'same-origin', method: 'GET'})
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                // console.log(data)
                // console.log(this.state)
                this.setState(() => (
                        this.state.questions = data.questions_images
                    )
                )

            })
            .catch((error) => console.log(error));

    }

    submitfunction(questionid, questionnumber) {
        let url = `/record${questionid}/?questionnumber=${questionnumber}`;
        // console.log(url);
        fetch(
            `/record${questionid}/?questionnumber=${questionnumber}`,
            {
                method: 'POST',
                credentials: 'same-origin',
                headers: {'Content_Type': 'application/json'},
                body: JSON.stringify({questionnumber: questionnumber})
            }
        )
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .catch((error) => console.log(error));
    }

    // likefunction(url, pid){
    //   fetch(
    //     `/api/v1/likes/?postid=${pid}`,
    //     {
    //       method: 'POST',
    //       credentials: 'same-origin',
    //       headers: {'Content_Type':'application/json'},
    //       body: JSON.stringify({postid:pid})
    //     }
    //   )
    //     .then((response) => {
    //       if (!response.ok) throw Error(response.statusText);
    //       return response.json();
    //     })
    //     .then((data) => {
    //       console.log(this.state.results)
    //       for (let i = 0; i < this.state.results.length; i++) {
    //         console.log(i)
    //         console.log(this.state.results[i])
    //         if (this.state.results[i].postid === pid) {
    //           console.log(data)
    //           this.setState((prevState) => (
    //             this.state.results[i].likes.numLikes = prevState.results[i].likes.numLikes + 1,
    //               this.state.results[i].likes.lognameLikesThis = !prevState.results[i].likes.lognameLikesThis,
    //               this.state.results[i].likes.url = data.url
    //           ));
    //         }
    //       }
    //     })
    //     .catch((error) => console.log(error));
    //
    // }
    //
    // unlikefunction(url, pid){
    //   console.log(url)
    //   fetch(
    //     url,
    //     {
    //       method: 'DELETE',
    //       credentials: 'same-origin'
    //     }
    //   )
    //     .then((response) => {
    //       if (!response.ok) throw Error(response.statusText);
    //       return response;
    //     })
    //     .then(() => {
    //       for (let i = 0; i < this.state.results.length; i++) {
    //         console.log(this.state.results)
    //         console.log(i)
    //         console.log(this.state.results[i])
    //         if (this.state.results[i].postid === pid) {
    //           console.log("UNLIK?E")
    //           this.setState((prevState) => (
    //             // console.log(prevState),
    //             this.state.results[i].likes.numLikes = prevState.results[i].likes.numLikes - 1
    //           ));
    //           this.setState((prevState) => (
    //             this.state.results[i].likes.lognameLikesThis = !prevState.results[i].likes.lognameLikesThis
    //           ));
    //           this.setState((prevState) => (
    //             this.state.results[i].likes.url = null
    //           ));
    //         }
    //       }
    //     })
    //     .catch((error) => console.log(error));
    //
    // }
    //
    // deleteComment(cid, pid) {
    //   for (let i = 0; i < this.state.results.length; i++) {
    //     if (this.state.results[i].postid === pid) {
    //       for (let j = 0; j < this.state.results[i].comments.length; j++) {
    //         if (this.state.results[i].comments[j].commentid === cid) {
    //           fetch(
    //             `/api/v1/comments/${cid}/`,
    //             {
    //               credentials: 'same-origin',
    //               method: 'DELETE',
    //               // headers: {'Content_Type':'application/json'},
    //               // body: JSON.stringify({commentid: cid})
    //             },
    //           )
    //             .then((response) => {
    //               if (!response.ok) throw Error(response.statusText);
    //               return response;
    //             })
    //           this.setState(
    //             this.state.results[i].comments.splice(j, 1)
    //           );
    //         }
    //       }
    //     }
    //   }
    // }
    //
    // addComment(newcomment, pid) {
    //   for (let i = 0; i < this.state.results.length; i++) {
    //     console.log(this.state.results[i].postid)
    //     if (this.state.results[i].postid === pid) {
    //       console.log("added")
    //       this.setState(prevState =>(
    //         prevState.results[i].comments = [...prevState.results[i].comments, newcomment]
    //       ));
    //
    //
    //     }
    //   }
    // }
    //
    // dbclick(pid){
    //   console.log(this.state)
    //   for (let i = 0; i < this.state.results.length; i++) {
    //     console.log(i)
    //     console.log(this.state.results[i])
    //     if (this.state.results[i].postid === pid) {
    //       if (!this.state.results[i].likes.lognameLikesThis){
    //         fetch(
    //           `/api/v1/likes/?postid=${pid}`,
    //           {
    //             method: 'POST',
    //             credentials: 'same-origin',
    //             headers: {'Content_Type':'application/json'},
    //             body: JSON.stringify({postid:pid})
    //           }
    //         )
    //           .then((response) => {
    //             if (!response.ok) throw Error(response.statusText);
    //             return response.json();
    //           })
    //           .then((data) => {
    //             this.setState((prevState) => (
    //               this.state.results[i].likes.numLikes = prevState.results[i].likes.numLikes + 1,
    //                 this.state.results[i].likes.lognameLikesThis = !prevState.results[i].likes.lognameLikesThis,
    //                 this.state.results[i].likes.url = data.url
    //             ));
    //           })
    //           .catch((error) => console.log(error));
    //       }
    //
    //     }
    //   }
    //
    //
    // }

    fetchData = () => {
        const {url} = this.props;
        console.log(url)
        // Call REST API to get the post's information
        fetch(url, {credentials: 'same-origin', method: 'GET'})
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                console.log(data)
                console.log(this.state)
                this.setState(() => (
                        this.state.questions = new Array(data.questions_images.length),
                            this.state.questions = [...data.questions_images]
                    )
                )

            })
            .catch((error) => console.log(error));

    };

    // mapStateToProps = state => ({
    //     posts: state.post.posts,
    //     page: state.post.page,
    //     postIds: state.post.postIds,
    //     isFetching: s

    // });

    render() {
        // This line automatically assigns this.state.imgUrl to the const variable imgUrl
        // and this.state.owner to the const variable owner
        const {questions} = this.state;
        // console.log(this.state)
        // const history = useHistory();
        // Render number of post image and post owner
        // let numLike;
        // if (result.likes.numLikes == 1) {
        //     numLike = <p style="font-weight: 500"> {result.likes.numLikes} like </p >
        // } else {
        //     numLike = <p style="font-weight: 500"> {result.likes.numLikes} likes </p >
        // }
        return (
            <div className="post">
                <InfiniteScroll
                    dataLength={10}
                    next={this.fetchData}
                    hasMore={false}
                    loader={<h4>更多题目加载中</h4>}
                    endMessage={
                        <p style={{textAlign: 'center'}}>
                            <b>您终于做完了</b>
                        </p>
                    }
                >
                    {this.state.questions.map((question, index) => (
                        // console.log("/images/" + question),
                            <article className="articleDef">
                                <p> Question:{index}</p>
                                <img src={"/images/" + question} alt={question}
                                     style={{
                                         paddingBottom: 10 + "px", paddingTop: 10 + "px",
                                         maxWidth: 100 + "%", height: "auto"
                                     }}
                                     className="imageDef"/>
                                <div className="reviews">
                                    <span>您认为下面的五行图片，从左到右的变化是 一致 的吗？</span>
                                    <Demo2 qn={index} qi={1}/>
                                    {/*{console.log(this.submitfunction, index)}*/}
                                    <span>您认为这种变化，大致上来讲，是否是某种 单一 的、容易理解、易于描述的变化？</span>
                                    <Demo2 qn={index} qi={2}/>
                                    {/*<form action={"/recordq2/?user="+index+"/"} method="post" encType="multipart/form-data">*/}
                                    {/*    <input type="hidden" name="operation" value="delete"/>*/}
                                    {/*    <input type="hidden" name="commentid" value="d"/>*/}
                                    {/*    <input type="radio" name="q2" value="yes"/> Yes/是*/}
                                    {/*    <input type="radio" name="q2" value="no"/> No/否 <br/>*/}
                                    {/*    <button type="submit">Submit</button>*/}
                                    {/*</form>*/}
                                </div>
                            </article>
                    ))}
                </InfiniteScroll>
            </div>
        );
    }
}

//
// class Post extends React.Component {
//   /* Display number of image and post owner of a single post
//    */
//
//   constructor(props) {
//     // Initialize mutable state
//     super(props);
//     this.state = { imgUrl: '', owner: '' };
//   }
//
//   componentDidMount() {
//     // This line automatically assigns this.props.url to the const variable url
//     const { url } = this.props;
//
//     // Call REST API to get the post's information
//     fetch(url, { credentials: 'same-origin' })
//       .then((response) => {
//         if (!response.ok) throw Error(response.statusText);
//         return response.json();
//       })
//       .then((data) => {
//         this.setState({
//           imgUrl: data.imgUrl,
//           owner: data.owner
//         });
//       })
//       .catch((error) => console.log(error));
//   }
//
//   render() {
//     // This line automatically assigns this.state.imgUrl to the const variable imgUrl
//     // and this.state.owner to the const variable owner
//     const { imgUrl, owner } = this.state;
//
//     // Render number of post image and post owner
//     return (
//       <div className="post">
//         < img src={imgUrl} />
//         <p>
//           {owner}
//         </p >
//       </div>
//     );
//   }
// }

Post.propTypes = {
    url: PropTypes.string.isRequired,
};

export default Post;