"use client"
import axios from 'axios';
import React, {useState, useCallback, useEffect} from 'react';
import {DndProvider, useDrag, useDrop} from 'react-dnd';
import {HTML5Backend} from 'react-dnd-html5-backend';
import {GripVertical} from 'lucide-react';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import {Input} from "@/components/ui/input";
import {Label} from "@/components/ui/label";
import {Button} from "@/components/ui/button";
import NexImage from 'next/image';

type RowData = {
    id: string;
    surname: string;
    constructor: string;
};

const initialRows: RowData[] = [
    {id: '1', surname: 'Verstappen', constructor: 'Red Bull'},
    {id: '2', surname: 'Norris', constructor: 'McLaren'},
    {id: '3', surname: 'Leclerc', constructor: 'Ferrari'},
    {id: '4', surname: 'Piastri', constructor: 'McLaren'},
    {id: '5', surname: 'Sainz', constructor: 'Ferrari'},
    {id: '6', surname: 'Colapinto', constructor: 'Mercedes'},
    {id: '7', surname: 'Russell', constructor: 'Mercedes'},
    {id: '8', surname: 'Pérez', constructor: 'Red Bull'},
    {id: '9', surname: 'Stroll', constructor: 'Aston Martin'},
    {id: '10', surname: 'Alonso', constructor: 'Aston Martin'},
    {id: '11', surname: 'Albon', constructor: 'Williams'},
    {id: '12', surname: 'Bearman', constructor: 'Ferrari'},
    {id: '13', surname: 'Tsunoda', constructor: 'RB F1 Team'},
    {id: '14', surname: 'Hülkenberg', constructor: 'Haas Ferrari'},
    {id: '15', surname: 'Ricciardo', constructor: 'RB F1 Team'},
    {id: '16', surname: 'Bottas', constructor: 'Sauber'},
    {id: '17', surname: 'Gasly', constructor: 'Alpine Renault'},
    {id: '18', surname: 'Guanyu', constructor: 'Sauber'},
    {id: '19', surname: 'Ocon', constructor: 'Alpine Renault'},
    {id: '20', surname: 'Hamilton', constructor: 'Mercedes'},
];

const DraggableTableRow = ({id, index, moveRow, children}: any) => {
    const [{isDragging}, ref] = useDrag({
        type: 'ROW',
        item: {id, index},
        collect: (monitor) => ({
            isDragging: monitor.isDragging(),
        }),
    });

    const [, drop] = useDrop({
        accept: 'ROW',
        hover: (draggedItem: any) => {
            if (draggedItem.index !== index) {
                moveRow(draggedItem.index, index);
                draggedItem.index = index;
            }
        },
    });

    return (
        <tr
            ref={(node) => ref(drop(node))}
            className={`hover:bg-gray-50 ${isDragging ? 'opacity-50' : ''}`}
        >
            {children}
        </tr>
    );
};

export default function Home() {
    // États pour les sélections
    const [date, setDate] = useState('');
    const [grandPrix, setGrandPrix] = useState('');
    const [rainfall, setRainfall] = useState('');
    const [humidity, setHumidity] = useState('');
    const [airTemp, setAirTemp] = useState('');

    // État pour les lignes de la table
    const [rows, setRows] = useState(initialRows);
    const [positions, setPositions] = useState([]);
    const [response, setResponse] = useState(null); // Nouvel état pour stocker la réponse


    // Fonction pour déplacer les lignes
    const moveRow = useCallback((dragIndex: number, hoverIndex: number) => {
        setRows((prevRows) => {
            const newRows = [...prevRows];
            const [draggedRow] = newRows.splice(dragIndex, 1);
            newRows.splice(hoverIndex, 0, draggedRow);
            return newRows;
        });
    }, []);

    // Mettre à jour les positions à chaque changement de `rows`
    useEffect(() => {
        setPositions(rows.map((row, index) => ({
            surname: row.surname,
            position: index + 1,
            constructor: row.constructor
        })));
    }, [rows]);

    // Fonction pour envoyer les données via POST
    const handleSubmit = async () => {

        const dataToSend = {
            date,
            grandPrix,
            rainfall: rainfall.replace(',', '.'),
            humidity,
            airTemp,
            positions,
        };

        try {
            const response = await axios.post('http://127.0.0.1:8080/predict', dataToSend);
            console.log('Réponse du serveur :', response.data);
            setResponse(response.data); // Mettre à jour l'état avec la réponse

        } catch (error) {
            console.error('Erreur lors de la requête POST :', error);
        }
    };

    return (
        <div>
            <header className="bg-red-600 text-white p-4 z-1">
                <div className="flex items-center max-w-6xl mx-auto gap-72">
                    <NexImage src="/F1_logo.jpg" alt="F1 Logo" width={150} height={100} className='z-10'/>
                    <h1 className="text-3xl font-bold text-center">F1 Race Prediction</h1>
                </div>
            </header>
            <div className='flex flex-col justify-center items-center mb-72'>

                <div className='flex '>
                    <div className='flex flex-col m-8 gap-5'>
                        <Select onValueChange={setDate}>
                            <SelectTrigger className="w-[180px]">
                                <SelectValue placeholder="Date"/>
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="2024">2024</SelectItem>
                            </SelectContent>
                        </Select>
                        <Select onValueChange={setGrandPrix}>
                            <SelectTrigger className="w-[180px]">
                                <SelectValue placeholder="Grand-Prix"/>
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="Azerbaijan">Azerbaijan</SelectItem>
                                <SelectItem value="Singapore">Singapore</SelectItem>
                                <SelectItem value="United States">United States</SelectItem>
                                <SelectItem value="Mexico">Mexico</SelectItem>
                                <SelectItem value="Brazil">Brazil</SelectItem>
                                <SelectItem value="Las Vegas">Las Vegas</SelectItem>
                                <SelectItem value="Qatar">Qatar</SelectItem>
                                <SelectItem value="Abu Dhabi">Abu Dhabi</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div>
                        <div className="grid w-full max-w-sm items-center gap-1.5 m-3">
                            <Label>Rainfall (number between 0 and 1)</Label>
                            <Input type="number" placeholder="Rainfall" onChange={(e) => setRainfall(e.target.value)}/>
                        </div>
                        <div className="grid w-full max-w-sm items-center gap-1.5 m-3">
                            <Label>Humidity</Label>
                            <Input type="number" placeholder="Humidity" onChange={(e) => setHumidity(e.target.value)}/>
                        </div>
                        <div className="grid w-full max-w-sm items-center gap-1.5 m-3">
                            <Label>AirTemp</Label>
                            <Input type="number" placeholder="AirTemp" onChange={(e) => setAirTemp(e.target.value)}/>
                        </div>
                    </div>
                </div>
                <DndProvider backend={HTML5Backend}>
                    <div className=" flex flex-col  container  p-4">
                        <h1 className="text-2xl font-bold flex justify-center mb-3">Starting grid</h1>
                        <div className="overflow-x-auto flex justify-center">
                            <table className=" border-collapse border border-gray-300 w-[1000px]">
                                <thead>
                                <tr className="bg-gray-100">
                                    <th className="border border-gray-300 p-2"></th>
                                    <th className="border border-gray-300 p-2">Position</th>
                                    <th className="border border-gray-300 p-2">Surname</th>
                                    <th className="border border-gray-300 p-2">Constructor</th>
                                </tr>
                                </thead>
                                <tbody>
                                {rows.map((row, index) => (
                                    <DraggableTableRow key={row.id} id={row.id} index={index} moveRow={moveRow}>
                                        <td className="border border-gray-300 p-2">
                                            <div className="flex items-center justify-center cursor-move"
                                                 title="Drag to reorder">
                                                <GripVertical className="text-gray-400" size={20}/>
                                            </div>
                                        </td>
                                        <td className="border border-gray-300 p-2">{index + 1}</td>
                                        <td className="border border-gray-300 p-2">{row.surname}</td>
                                        <td className="border border-gray-300 p-2">{row.constructor}</td>
                                    </DraggableTableRow>
                                ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </DndProvider>
                <Button className='mt-10 w-[200px] text-xl' variant="destructive"
                        onClick={handleSubmit}>Predict</Button>
                {response && (
                    <div className="mt-4 p-4 border border-gray-300 rounded">
                        <h2 className="text-xl font-bold">Predicted Positions:</h2>
                        <ul>
                            {response.predicted_positions.map((position: string, index: number) => (
                                <li key={index}>{index} : {position}</li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </div>
    );
}
