import React from 'react';
import { useEffect, useRef, useState } from 'react';
import Tree from 'react-d3-tree';
import { useSearchParams } from 'react-router-dom';
import useSWR from 'swr';
import { getQuery } from '../api';
import data from "../db/db.json";

const renderNodeWithCustomEvents = ({
    nodeDatum,
    handleNodeHover,
    handleNodeClick
}) => (
    <g>
        <rect width="240" height="60" x="-120" y="-30" fill="#B5DAFF" rx="10" ry="10" strokeWidth="2" onClick={() => handleNodeClick()} onMouseOver={() => handleNodeHover(nodeDatum)} />
        <text fill="black" strokeWidth="1" x="-20" y="-3">
            {nodeDatum.name}
        </text>
        <text fill="black" strokeWidth="1" x="-80" y="18" fontSize="10px">
            * Hover for details, Click to return
        </text>
    </g>
);


function Graph(props) {
    const ref = useRef(null);
    const [height, setHeight] = useState(0);
    const [width, setWidth] = useState(0);
    const [searchParams] = useSearchParams();
    const q = searchParams.get('question');
    const { data: chartData } = useSWR(q && `/query/${q}`, () => getQuery(q || ''), {
        revalidateIfStale: false,
        revalidateOnFocus: false,
        revalidateOnReconnect: false,
    });
    // const chartData = JSON.parse(JSON.stringify(data));
    useEffect(() => {
        setHeight(ref.current.offsetHeight);
        setWidth(ref.current.offsetWidth);
        if (!chartData && !q) props.setAnswer('Please ask any questions you may have!')
        else if (!chartData) props.setAnswer('Loading...')
        else props.setAnswer(fullAnswer);
    }, [chartData, q]);
    if (!chartData) return (<div id="treeWrapper" ref={ref} style={{ margin: '0', padding: '0', width: '100%', height: '100%' }} />)
    const tempChart = {
        name: '',
        attributes: {
            subQuestion: '',
            subAnswer: '',
            top5List: []
        },
        children: [],
    };
    const makeChart = (stepCount, chartData, target) => {
        if (stepCount === 0) {
            target.name = "Step" + String(stepCount + 1);
            target.attributes.subQuestion = chartData["nodeList"][stepCount]["subQuestion"];
            target.attributes.subAnswer = chartData["nodeList"][stepCount]["subAnswer"];
            for (var i = 0; i < 5; i++) {
                var node = {
                    first: chartData["nodeList"][stepCount]["top5List"][i]["first"],
                    second: chartData["nodeList"][stepCount]["top5List"][i]["second"]
                };
                target.attributes.top5List.push(node);
            }
            makeChart(stepCount + 1, chartData, target)
            return;
        }
        if (stepCount < chartData["stepCount"]) {
            const temp = {
                name: '',
                attributes: {
                    subQuestion: '',
                    subAnswer: '',
                    top5List: []
                },
                children: [],
            };
            temp.name = "Step" + String(stepCount + 1);
            temp.attributes.subQuestion = chartData["nodeList"][stepCount]["subQuestion"];
            temp.attributes.subAnswer = chartData["nodeList"][stepCount]["subAnswer"];
            for (var i = 0; i < 5; i++) {
                var node = {
                    first: chartData["nodeList"][stepCount]["top5List"][i]["first"],
                    second: chartData["nodeList"][stepCount]["top5List"][i]["second"]
                };
                temp.attributes.top5List.push(node);
            }
            target.children.push(temp);
            makeChart(stepCount + 1, chartData, target.children[0]);
            return;
        }
        return;
    };
    chartData && makeChart(0, chartData, tempChart);
    const orgChart = tempChart;
    const question = "Q: " + chartData["query"];
    var fullAnswer = question + "\n\n";
    for (var step = 0; step < chartData["stepCount"]; step++) {
        const subQuestion = "Step" + String(step + 1) + "\nQ: " + chartData["nodeList"][step]["subQuestion"];
        const subAnswer = "A: " + chartData["nodeList"][step]["subAnswer"];
        fullAnswer += (subQuestion + "\n" + subAnswer + "\n\n");
    }
    fullAnswer += chartData["finalExplanation"] + "\n\n" + chartData["finalAnswer"];

    const handleNodeHover = (nodeDatum) => {
        var text = "SubQ: " + nodeDatum.attributes.subQuestion + "\n\nSubA: " + nodeDatum.attributes.subAnswer + "\n\n";
        for (var i = 0; i < 5; i++) {
            var topList = "Document" + String(i + 1) + "\n";
            topList += nodeDatum.attributes.top5List[i].second + "\n" + "Document URL: " + nodeDatum.attributes.top5List[i].first + "\n";
            text += topList + "\n"
        }
        props.setAnswer(text);
    };
    const handleNodeClick = () => {
        const text = fullAnswer;
        props.setAnswer(text);
    };

    return (
        <div id="treeWrapper" ref={ref} style={{ margin: '0', padding: '0', width: '100%', height: '100%' }}>
            <Tree
                data={orgChart}
                orientation="vertical"
                translate={{ x: width / 2, y: height / 4.5 }}
                renderCustomNodeElement={(rd3tProps) =>
                    renderNodeWithCustomEvents({ ...rd3tProps, handleNodeHover, handleNodeClick })
                }
            />
        </div>
    );
}

export default Graph;