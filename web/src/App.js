import React, { Component } from 'react';
import './App.css';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.css';

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      formData: {
        InputSentence: '我一把把把把住了',
        SegModel: 'bimm',
      },
      result: ""
    };
  }

  handleChange = (event) => {
    const value = event.target.value;
    const name = event.target.name;
    var formData = this.state.formData;
    formData[name] = value;
    this.setState({
      formData
    });
  }

  handlePredictClick = (event) => {
    const formData = this.state.formData;
    this.setState({ isLoading: true });
    fetch('http://127.0.0.1:5000/prediction/',
      {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .then(response => {
        this.setState({
          result: response.result,
          isLoading: false
        });
      });
  }

  handleCancelClick = (event) => {
    this.setState({ result: "" });
  }

  render() {
    const isLoading = this.state.isLoading;
    const formData = this.state.formData;
    const result = this.state.result;

    return (
      <Container>
        <div>
          <h1 className="title">Chinese Word Segmentation</h1>
        </div>
        <div className="content">
          <Form>
            <Form.Row>
              <Form.Group as={Col}>
                <Form.Label>Input Sentence</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="eg.`柳奶奶和牛奶奶泼牛奶吓坏了刘奶奶`"
                  name="InputSentence"
                  value={formData.InputSentence}
                  onChange={this.handleChange} />
              </Form.Group>

            </Form.Row>
            <Form.Row>
              <Form.Group as={Col}>
                <Form.Label>Choose Model</Form.Label>
                <Form.Control
                  as="select"
                  value={formData.SegModel}
                  name="SegModel"
                  onChange={this.handleChange}>
                  <option>all</option>
                  <option>fmm</option>
                  <option>bmm</option>
                  <option>bimm</option>
                  <option>mmseg</option>
                  <option>hmm</option>
                  <option>bilstm-crf</option>
                  <option>bert-crf</option>
                  <option>jieba</option>
                  <option>thulac</option>
                  <option>ltp</option>
                  <option>hanlp</option>
                </Form.Control>
              </Form.Group>
            </Form.Row>
            <Row>
              <Col>
                <Button
                  block
                  variant="success"
                  disabled={isLoading}
                  onClick={!isLoading ? this.handlePredictClick : null}>
                  {isLoading ? 'Segmenting' : 'Segment'}
                </Button>
              </Col>
              <Col>
                <Button
                  block
                  variant="danger"
                  disabled={isLoading}
                  onClick={this.handleCancelClick}>
                  Clear Segmentation
                </Button>
              </Col>
            </Row>
          </Form>
          {result === "" ? null :
            (<Row>
              <Col className="result-container">
                <h5><pre align="left">{result}</pre></h5>
              </Col>
            </Row>)
          }
        </div>
      </Container>
    );
  }
}

export default App;